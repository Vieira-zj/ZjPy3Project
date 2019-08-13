# -*- coding: utf-8 -*-
'''
Created on 2019-08-13
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
/mnt/spark_dir/data_prepare02.py
'''

import datetime
import random

import pyspark
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import HiveContext


def print_df_info(pyspark_df):
    print('\nDATAFRAME INFO:')
    print('data schema:')
    pyspark_df.printSchema()
    print('records count: %d' % pyspark_df.count())
    print('top 10 records:')
    pyspark_df.show(10)


class DataCreate(object):

    def __init__(self, sc, sqlContext, hiveContext):
        self._sc = sc
        self._sqlContext = sqlContext
        self._hiveContext = hiveContext

    def data_prepare(self, write_path, row_count, dt, dt_n, part_n=1, f_type='parquet'):
        '''
        Create parquet or orc files partitioned by dt (date).
        '''
        schema = ['id', 'flag']
        write_path = self._format_path(write_path)
        dt_timestamp = datetime.datetime.strptime(dt, '%Y%m%d')

        start = 0
        for i in range(dt_n):
            test_rdd = self._sc.parallelize(range(start, start+row_count), part_n) \
                .map(lambda x: [x, str(x) + random.choice('yn')])
            test_df = self._hiveContext.createDataFrame(test_rdd, schema)

            dt = datetime.datetime.strftime(dt_timestamp + datetime.timedelta(days=i), '%Y%m%d')
            if f_type == 'orc':
                test_df.write.orc(write_path + dt)
            else:
                test_df.write.parquet(write_path + dt)

            start += row_count

    def _format_path(self, path):
        if path.endswith('/'):
            path += 'dt='
        else:
            path += '/dt='
        return path
# end class


class DataLoad(object):

    def __init__(self, sc, sqlContext, hiveContext):
        self._sc = sc
        self._sqlContext = sqlContext
        self._hiveContext = hiveContext

    def _pre_load(self, d_path, s_date, e_date):
        d_path = self._format_path(d_path)
        f_paths = [d_path + s_date]

        s_date_timestamp = datetime.datetime.strptime(s_date, '%Y%m%d')
        e_date_timestamp = datetime.datetime.strptime(e_date, '%Y%m%d')
        while s_date_timestamp <= e_date_timestamp:
            f_paths.append(d_path + datetime.datetime.strftime(s_date_timestamp, '%Y%m%d'))
            s_date_timestamp += datetime.timedelta(days=1)

        return f_paths

    def _format_path(self, path):
        if path.endswith('/'):
            path += 'dt='
        else:
            path += '/dt='
        return path

    def load_data(self, d_path, s_date, e_date, f_type='parquet'):
        '''
        Load data from parquet or orc files by dt (start_date, end_date).
        '''
        f_paths = self._pre_load(d_path, s_date, e_date)
        if len(f_paths) == 0:
            raise Exception("Dataload is not init!")

        reader = None
        if f_type == 'orc':
            reader = self._hiveContext.read.orc
        else:
            reader = self._sqlContext.read.parquet

        read_dfs = []
        for f_path in f_paths:
            try:
                df = reader(f_path)
            except Exception as e:
                print(e)
                continue
            read_dfs.append(df)

        ret_df = read_dfs[0]
        for i in range(1, len(read_dfs)):
            ret_df = ret_df.unionAll(df)
        return ret_df
# end class


def testDataPrepareForParquet(sc, sqlContext, hiveContext):
    d_path = 'hdfs:///user/root/test/test_parquet/'
    start_date = '20190701'

    dataCreate = DataCreate(sc, sqlContext, hiveContext)
    dataCreate.data_prepare(d_path, 10000, start_date, 3, f_type='parquet')

    load = DataLoad(sc, sqlContext, hiveContext)
    df = load.load_data(d_path, start_date, '20190703')
    print_df_info(df)
    # output:
    # /user/root/test/test_parquet/dt=20190701
    # /user/root/test/test_parquet/dt=20190702
    # /user/root/test/test_parquet/dt=20190703


def testDataPrepareForOrc(sc, sqlContext, hiveContext):
    d_path = 'hdfs:///user/root/test/test_orc/'
    start_date = '20190701'

    dataCreate = DataCreate(sc, sqlContext, hiveContext)
    dataCreate.data_prepare(d_path, 10000, start_date, 3, f_type='orc')

    load = DataLoad(sc, sqlContext, hiveContext)
    df = load.load_data(d_path, start_date, '20190703', f_type='orc')
    print_df_info(df)
    # output:
    # /user/root/test/test_orc/dt=20190701
    # /user/root/test/test_orc/dt=20190702
    # /user/root/test/test_orc/dt=20190703


if __name__ == '__main__':

    conf = SparkConf().setAppName('data_prepare_demo').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    print('pyspark version: ' + str(sc.version))
    sqlContext = SQLContext(sc)
    hiveContext = HiveContext(sc)

    # testDataPrepareForParquet(sc, sqlContext, hiveContext)
    testDataPrepareForOrc(sc, sqlContext, hiveContext)

    print('pyspark data prepare demo DONE.')
