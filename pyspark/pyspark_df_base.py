# -*- coding: utf-8 -*-
'''
Created on 2019-04-25
@author: zhengjin

cmd for submit spark job:
bin/spark-submit \
--master yarn-client \
--driver-memory 1g \
--executor-memory 1g \
--executor-cores 1 \
/mnt/spark_dir/pyspark_df_base.py

NOTE: 
spark shuffle asks for more memory, and in docker engine, update limited memory to 3G (2G is default)!
'''

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext


# read hdfs file
def pyspark_df_demo01(sqlContext):
    print('read hdfs json file =>')
    # {"name":"Michael"}
    # {"name":"Andy", "age":30}
    # {"name":"Justin", "age":19}
    df_01 = sqlContext.read.format('json').load('/user/root/test/people.json')
    print('data schema: ' + str(df_01.dtypes))
    print('people count: ' + str(df_01.count()))
    print('people info:')
    df_01.show()

    # java.lang.ClassNotFoundException: Failed to find data source: com.databricks.spark.csv.
    print('read hdfs csv file =>')
    # name,age
    # Michael,37
    # Andy,30
    # Justin,19
    df_02 = sqlContext.read.format('com.databricks.spark.csv').options(
        header='true', inferschema='true').load('/user/root/test/people.csv')
    print('data schema:')
    df_02.printSchema()
    print('people count: ' + str(df_02.count()))
    print('people info:')
    df_02.show()


# init a dataframe and query
def pyspark_df_demo02(sqlContext):
    records = []
    records.append((1, 'age', '30', 50, 40))
    records.append((1, 'city', 'beijing', 50, 40))
    records.append((1, 'gender', 'fale', 50, 40))
    records.append((1, 'height', '172cm', 50, 40))
    records.append((1, 'weight', '70kg', 50, 40))

    records.append((2, 'age', '26', 100, 80))
    records.append((2, 'city', 'beijing', 100, 80))
    records.append((2, 'gender', 'fale', 100, 80))
    records.append((2, 'height', '170cm', 100, 80))
    records.append((2, 'weight', '65kg', 100, 80))

    schema = ['user_id', 'attr_name', 'attr_value', 'income', 'expenses']
    df = sqlContext.createDataFrame(records, schema)
    print('data schema:')
    df.printSchema()
    print('user count: ' + str(df.count()))
    print('users info:')
    df.show(5)

    # do shuffle for 'distinct'
    print('[distinct output] user ids:')
    df.select('user_id').distinct().show()

    print('[select output] user info with income=50:')
    df.select('user_id', 'attr_value', 'income').where('income=50').show()

    print('[orderby output] user info with income desc seq:')
    df.orderBy(df.income.desc()).show()

    print('[col add output] user info with new income:')
    df.withColumn('income_new', df.income+10).show(5)


# dataframe sql
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

    print('swimmers:')
    df.show()

    print('[select output] get swimmers ids with age=22 by str:')
    df.select('id', 'age').filter('age=22').show()
    print('[select output] get swimmers ids with age=22 by type:')
    df.select(df.id, df.age).filter(df.age == 22).show()

    print('[select output] get swimmers ids with age=22 by str sql:')
    df.registerTempTable('swimmers')
    sqlContext.sql('select id,age from swimmers where age=22').show()

    print('[like output] get swimmers names with eye color startwith "b":')
    df.select('name', 'eyeColor').filter('eyeColor like "b%"').show()
    print('[like output] get swimmers names with eye color startwith "b" by str sql:')
    str_sql = 'select name,eyeColor from swimmers where eyeColor like "b%"'
    sqlContext.sql(str_sql).show()


# dataframe join
def pyspark_df_demo04(sqlContext):
    # same data schema for 2 dataframe
    df_01 = sqlContext.createDataFrame((
        (1, 'asf'),
        (2, '2143'),
        (3, 'rfds')
    )).toDF('label', 'sentence')
    print('df_01 data:')
    df_01.show()

    df_02 = sqlContext.createDataFrame((
        (1, 'asf'),
        (2, '2143'),
        (4, 'f8934y')
    )).toDF('label', 'sentence')
    print('df_02 data:')
    df_02.show()

    # 差集
    print('subtract output:')
    df = df_02.select('sentence').subtract(df_01.select('sentence'))
    df.show()

    # 交集
    print('intersect output:')
    df = df_02.select('sentence').intersect(df_01.select('sentence'))
    df.show()

    # 并集
    print('union output:')
    df = df_02.select('sentence').unionAll(df_01.select('sentence'))
    df.show()


# dataframe join
def pyspark_df_demo05(sc):
    from pyspark.sql import Row

    rdd = sc.parallelize(
        [Row(name='Alice', age=5, height=80), Row(name='Tom', age=10, height=70)])
    df_01 = rdd.toDF()
    print('df_01 data:')
    df_01.show()

    rdd = sc.parallelize([Row(name='Alice', weight=45), Row(name='Jim', weight=37)])
    df_02 = rdd.toDF()
    print('df_02 data:')
    df_02.show()

    # do shuffle for 'join'
    print('left join output:')
    df_01.join(df_02, df_01.name == df_02.name, 'left').show()

    # print('inner join output:')
    # df_01.join(df_02, df_01.name == df_02.name, 'inner').show()


if __name__ == '__main__':

    conf = SparkConf().setAppName('pyspark_df_base_test').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    print('pyspark version: ' + str(sc.version))
    sqlContext = SQLContext(sc)

    pyspark_df_demo04(sqlContext)
    # pyspark_df_demo05(sc)
    print('pyspark dataframe base demo DONE.')
