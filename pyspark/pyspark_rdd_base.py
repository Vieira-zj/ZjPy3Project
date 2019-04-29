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


# pair rdd
def pyspark_rdd_demo05(sc):
    rdd = sc.parallelize(['Hello hello', 'Hello New York', 'York says hello'])
    result_rdd = rdd.flatMap(lambda sentence: sentence.split(' ')) \
        .map(lambda word: word.lower()) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda x, y: x + y).cache()

    print('\nword count result: ' + str(result_rdd.collect()))
    print('\nword count result as map: ' + str(result_rdd.collectAsMap()))

    seq_rdd = result_rdd.sortByKey(ascending=True)
    print('\nfirst 2 word count: ' + str(seq_rdd.take(2)))

    top_rdd = result_rdd.sortBy(lambda x: x[1], ascending=False)
    print('\ntop 2 word count: ' + str(top_rdd.take(2)))


# rdd join
def pyspark_rdd_demo06(sc):
    num_rdd_01 = sc.parallelize([1, 2, 3]).cache()
    num_rdd_02 = sc.parallelize([2, 3, 4]).cache()

    # 并集
    union_rdd = num_rdd_01.union(num_rdd_02)
    print('\nrdds union result: ' + str(union_rdd.collect()))
    # 交集
    intersection_rdd = num_rdd_01.intersection(num_rdd_02)
    print('\nrdds intersection result: ' + str(intersection_rdd.collect()))
    # 差集
    subtract_rdd = num_rdd_01.subtract(num_rdd_02)
    print('\nrdds subtract result: ' + str(subtract_rdd.collect()))


# pair rdd join
def pyspark_rdd_demo07(sc):
    home_rdd = sc.parallelize([
        ('Brussels', 'John'),
        ('Brussels', 'Jack'),
        ('Leuven', 'Jane'),
        ('Antwerp', 'Jill'),
    ]).cache()

    quality_rdd = sc.parallelize([
        ('Brussels', 10),
        ('Antwerp', 7),
        ('RestOfFlanders', 5),
    ]).cache()

    result_rdd = home_rdd.join(quality_rdd)
    print('\ninner join result: ' + str(result_rdd.collect()))

    result_rdd = home_rdd.leftOuterJoin(quality_rdd)
    print('\nleft join result: ' + str(result_rdd.collect()))


# cache
def pyspark_rdd_demo08(sc):
    # import numpy as np
    # num_rdd = sc.parallelize(np.linspace(1.0, 10.0, 10))

    num_rdd = sc.parallelize([1.0, 2.0, 3.0, 4.0, 5.0])
    squares_rdd = num_rdd.map(lambda x: x**2).cache()

    avg = squares_rdd.reduce(lambda x, y: x + y) / squares_rdd.count()
    print('\naverage value: ' + str(avg))


if __name__ == '__main__':

    conf = SparkConf().setAppName('pyspark_rdd_base_test').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    print('pyspark version: ' + str(sc.version))

    pyspark_rdd_demo08(sc)
    print('pyspark rdd base demo DONE.')
