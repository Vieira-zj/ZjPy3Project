# -*- coding: utf-8 -*-
'''
Created on 2019-04-25
@author: zhengjin

cmd for submit spark job:
bin/spark-submit \
--class org.apache.spark.examples.SparkPi \
--master yarn-client \
--driver-memory 1g \
--executor-memory 1g \
--executor-cores 1 \
/mnt/spark_dir/pyspark_df_base.py
'''

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext


# init a dataframe
def pyspark_df_demo01(sqlContext):
    records = []
    records.append((1, 'age', '30', 50, 40))
    records.append((1, 'city', 'beijing', 50, 40))
    records.append((1, 'gender', 'fale', 50, 40))
    records.append((1, 'height', '172cm', 50, 40))
    records.append((1, 'weight', '70kg', 50, 40))

    schema = ['user_id', 'attr_name', 'attr_value', 'income', 'expenses']
    df = sqlContext.createDataFrame(records, schema)
    print('data schema: ' + str(df.dtypes))
    print('user count: ' + str(df.count()))
    print('users info:')
    df.show()


# read hdfs json file
def pyspark_df_demo02(sqlContext):
    df = sqlContext.read.format('json').load('/user/root/test/people.json')
    # {"name":"Michael"}
    # {"name":"Andy", "age":30}
    # {"name":"Justin", "age":19}
    print('data schema: ' + str(df.dtypes))
    print('people count: ' + str(df.count()))
    print('people info:')
    df.show()


# select in dataframe
def pyspark_df_demo03(sqlContext):
    from pyspark.sql.types import StructType, StructField, StringType, LongType

    records = []
    records.append((100, 'Katie', 19, 'brown'))
    records.append((101, 'Michael', 22, 'green'))
    records.append((102, 'Simone', 23, 'blue'))

    schema = StructType([
        StructField('id', LongType(), True),
        StructField('name', StringType(), True),
        StructField('age', LongType(), True),
        StructField('eyeColor', StringType(), True)
    ])

    df = sqlContext.createDataFrame(records, schema)
    print('data schema: ' + str(df.dtypes))
    print('swimmers count: ' + str(df.count()))

    print('[select output]: get swimmers ids with age=22 by str:')
    df.select('id', 'age').filter('age=22').show()
    print('[select output]: get swimmers ids with age=22 by type:')
    df.select(df.id, df.age).filter(df.age == 22).show()

    print('[select output]: get swimmers ids with age=22 by str sql:')
    df.registerTempTable('swimmers')
    sqlContext.sql('select id,age from swimmers where age=22').show()


if __name__ == '__main__':

    conf = SparkConf().setAppName('pyspark_df_base_test').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    pyspark_df_demo01(sqlContext)
    print('pyspark dataframe base demo DONE.')
