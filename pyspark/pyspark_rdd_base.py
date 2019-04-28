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
/mnt/spark_dir/pyspark_rdd_base.py
'''

from pyspark import SparkConf, SparkContext


# init a rdd
def pyspark_rdd_demo01(sc):
    ls_rdd = sc.parallelize([i for i in range(60)]).cache()
    print('rdd partitions size: %d' % ls_rdd.getNumPartitions())

    map_output = ls_rdd.map(lambda x: x+2).collect()
    print('map output: ' + str(map_output))
    filter_output = ls_rdd.filter(lambda x: x % 2 == 0).collect()
    print('filter output: ' + str(filter_output))


# distinct
def pyspark_rdd_demo02(sc):
    def _doubleIfOdd(x):
        return x if x % 2 == 0 else x * 2

    num_rdd = sc.parallelize(range(1, 11))
    result_rdd = num_rdd.map(_doubleIfOdd) \
        .filter(lambda x: x > 6) \
        .distinct()
    print('result rdd: ' + str(result_rdd.collect()))


# read hdfs text file
def pyspark_rdd_demo03(sc):
    # pre-condition: mkdir and put file on hdfs
    hdfs_path = '/user/root/wordcount/helloworld.txt'
    rdd = sc.textFile(hdfs_path).cache()
    print('lines count: %d' % rdd.count())
    print('first line output: ' + rdd.first())


# wordcount example
def pyspark_rdd_demo04(sc):
    from operator import add

    hdfs_path = '/user/root/wordcount/helloworld.txt'
    rdd = sc.textFile(hdfs_path)
    counts = rdd.flatMap(lambda x: x.split(' ')) \
        .map(lambda x: (x, 1)).reduceByKey(add)

    for (word, count) in counts.collect():
        print('%s: %d' % (word, count))


if __name__ == '__main__':

    conf = SparkConf().setAppName('pyspark_rdd_base_test').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    print('pyspark version: ' + str(sc.version))

    pyspark_rdd_demo04(sc)
    print('pyspark rdd base demo DONE.')
