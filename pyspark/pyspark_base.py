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
/mnt/ds_test/pyspark_base.py
'''

from pyspark import SparkConf, SparkContext


# init a rdd
def pyspark_demo01(sc):
    ls_rdd = sc.parallelize([i for i in range(60)])
    print('rdd partitions size: ' + ls_rdd.getNumPartitions())
    print('output:' + ls_rdd.map(lambda x: x+2).collect())


# read hdfs text file
def pyspark_demo02(sc):
    # pre-condition: put file to hdfs
    hdfs_path = '/user/root/wordcount/helloworld.txt'
    rdd = sc.textFile(hdfs_path)
    print('first line output: ' + rdd.first())


# wordcount example
def pyspark_demo03(sc):
    from operator import add

    hdfs_path = '/user/root/wordcount/helloworld.txt'
    rdd = sc.textFile(hdfs_path)
    counts = rdd.flatMap(lambda x: x.split(" ")) \
        .map(lambda x: (x, 1)).reduceByKey(add)

    for (word, count) in counts.collect():
        print('%s: %d' % (word, count))


if __name__ == "__main__":

    conf = SparkConf().setAppName('pyspark_base_test').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    print('pyspark version: ' + str(sc.version))

    pyspark_demo03(sc)

    print('pyspark base demo DONE.')
