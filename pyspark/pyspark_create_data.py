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
/mnt/spark_dir/pyspark_create_data.py
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


# demo01: create data for tbl_account
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


def create_data_demo01():
    print('generate id_account_list')
    num_account = 1500
    id_account_rdd = sc.parallelize(range(num_account), 1) \
        .map(lambda x: gen_evt_id('acc'))
    id_account_rdd.persist(storageLevel=pyspark.StorageLevel.MEMORY_AND_DISK)

    print('extend tbl_account by account_ids')
    tbl_account, schema_account = extend_tbl_account(id_account_rdd)
    tbl_account_df = sqlContext.createDataFrame(tbl_account, schema_account)

    print('\nDATA INFO:')
    print('data schema:')
    tbl_account_df.printSchema()
    print('total id_accounts: ' + str(tbl_account_df.count()))
    print('top 5 id_accounts:')
    tbl_account_df.show(5)

    prefix = 'hdfs:///user/root/test/'
    tbl_account_df.write.parquet(prefix + '/account')
    id_account_rdd.unpersist()
    print('generate id_account_list success')

    # outputs:
    # hdfs dfs -ls -h /user/root/test/account
    # 0 2019-05-22 10:21 /user/root/test/account/_SUCCESS
    # 39.1 K 2019-05-22 10:21 /user/root/test/account/part-r-00000-7523b316-5d48-46db-8bf4-8c74ce1ef3ec.gz.parquet
# demo01 end


# demo02: create data for id_list
def create_data_demo02():
    pass


if __name__ == '__main__':

    conf = SparkConf().setAppName('pyspark_create_data_demo').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    print('pyspark version: ' + str(sc.version))
    sqlContext = SQLContext(sc)

    create_data_demo01()
    print('pyspark create data demo DONE.')
