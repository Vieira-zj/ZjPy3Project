# -*- coding: utf-8 -*-
'''
Created on 2019-05-22
@author: zhengjin

Conditions:
$ hdfs dfs -mkdir -p /user/root/test

Submit spark job:
bin/spark-submit \
--master yarn-client \
--driver-memory 1g \
--num-executors 1 \
--executor-memory 1g \
--executor-cores 2 \
/mnt/spark_dir/pyspark_data_handler.py
'''

import random
import uuid
import pyspark
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext


TYPE_LIST = 'abcdefghijklmnopqrstuvwxyz'
FLAG_LIST = map(str, range(2))


def gen_evt_id(prefix):
    return prefix + '_' + str(uuid.uuid4())


def print_df_info(pyspark_df):
    print('\nDATA INFO:')
    print('data schema:')
    pyspark_df.printSchema()
    print('total id_accounts: ' + str(pyspark_df.count()))
    print('top 5 id_accounts:')
    pyspark_df.show(5)


# demo01: generate and write data
def extend_tbl_account(id_account_rdd):

    def _extend_acount(account_id):
        account_type = 'acc_' + random.choice(TYPE_LIST)
        offshore = random.choice(FLAG_LIST)
        open_date = '2017-0%d-%d' % (random.randint(1, 9), random.randint(10, 30))
        close_date = '2019-0%d-%d' % (random.randint(1, 9), random.randint(10, 30))
        return [account_id, account_type, offshore, open_date, close_date]

    result = id_account_rdd.map(lambda x: _extend_acount(x))
    schema = ['account_id', 'account_type', 'offshore', 'open_date', 'close_date']
    return result, schema


def pyspark_data_demo01():
    print('generate id_account_list')
    num_account = 1500
    id_account_rdd = sc.parallelize(range(num_account), 1) \
        .map(lambda x: gen_evt_id('acc'))
    id_account_rdd.persist(storageLevel=pyspark.StorageLevel.MEMORY_AND_DISK)

    print('extend tbl_account by account_ids')
    tbl_account, schema_account = extend_tbl_account(id_account_rdd)
    tbl_account_df = sqlContext.createDataFrame(tbl_account, schema_account)
    print_df_info(tbl_account_df)

    prefix = 'hdfs:///user/root/test/'
    tbl_account_df.write.parquet(prefix + '/account')
    id_account_rdd.unpersist()
    print('write id_account_list success')

    # outputs:
    # hdfs dfs -ls -h /user/root/test/account
    # /user/root/test/account/_SUCCESS
    # /user/root/test/account/part-r-00000-7523b316-5d48-46db-8bf4-8c74ce1ef3ec.gz.parquet


# demo02: read and rewrite data
def pyspark_data_demo02():
    import pyspark.sql.functions as F
    import pyspark.sql.types as T

    def add_index(col1, col2):
        return col1 + '_' + str(int(col2))
    udf_add_index = F.udf(add_index, T.StringType())

    # read records from parquet
    home_dir = 'hdfs:///user/root/test/account/'
    parquet_file = 'part-r-00000-7523b316-5d48-46db-8bf4-8c74ce1ef3ec.gz.parquet'
    print('read id_account_list parquet file: ' + home_dir + parquet_file)
    id_account_df = sqlContext.read.parquet(home_dir + parquet_file)
    id_account_df.persist(storageLevel=pyspark.StorageLevel.MEMORY_AND_DISK)
    print_df_info(id_account_df)
    print('read id_account_list success')

    # 产生额外分片
    write_dir = 'hdfs:///user/root/test/new_account/'
    for i in range(2, 4):
        new_id_account_df = id_account_df.withColumn('tmp_index', F.lit(i)) \
            .withColumn('new_id', udf_add_index('account_id', 'tmp_index')) \
            .drop('account_id') \
            .drop('tmp_index') \
            .withColumnRenamed('new_id', 'account_id')
        print('new partition #' + str(i))
        print_df_info(new_id_account_df)

        new_id_account_df.write.mode('overwrite').parquet(
            write_dir + 'account_' + str(i))
        print('write new id_account_list success')

    id_account_df.unpersist()

    # outputs:
    # /user/root/test/new_account/account_2/_SUCCESS
    # /user/root/test/new_account/account_2/part-r-00000-d3427ae9-dbb9-49a6-9228-f68ca8e1ef38.gz.parquet
    # /user/root/test/new_account/account_3/_SUCCESS
    # /user/root/test/new_account/account_3/part-r-00000-57715fe2-9f00-486f-863d-2c3a9fa510e7.gz.parquet


if __name__ == '__main__':

    conf = SparkConf().setAppName('pyspark_create_data_demo').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    print('pyspark version: ' + str(sc.version))
    sqlContext = SQLContext(sc)

    # pyspark_data_demo01()
    pyspark_data_demo02()
    print('pyspark data handler demo DONE.')
