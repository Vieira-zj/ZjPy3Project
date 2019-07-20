# -*- coding: utf-8 -*-
'''
Created on 2019-05-26
@author: zhengjin
'''

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series, DataFrame


def pandas_series_demo01():
    # create series
    print('series with default index:\n', Series([1, 2, 3, 4]))  # 默认索引（从0到N-1）

    print('series with index:\n', Series(range(4), index=['a', 'b', 'c', 'd']))

    dict_data = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
    print('series by dict:\n', Series(dict_data))

    states = ['California', 'Ohio', 'Oregon', 'Texas']
    ser = Series(dict_data, index=states)
    print('series by dict and index:\n', ser)
    print('series in null:\n', pd.isnull(ser))
    print('series not null:\n', pd.notnull(ser))


def pandas_series_demo02():
    # get index and value
    ser = Series(range(4), index=['a', 'b', 'c', 'd'])
    print('series item at loc 0:', ser[0])
    print('series item at idx "b":', ser['b'])
    print('series item at idx "a" and "c":\n', ser[['a', 'c']])

    print('series index:\n', ser.index)
    print('series values:\n', ser.values)


def pandas_series_demo03():
    # operation on series
    ser = Series(range(4), index=['a', 'b', 'c', 'd'])
    print('series, items > 1:\n', ser[ser > 1])
    print('series, items * 2:\n', ser * 2)
    print('square series:\n', np.square(ser))
    print('series, sum by rows:\n', ser.cumsum())

    # 相同索引值的元素相加
    dict_data = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
    ser1 = Series(dict_data)
    states = ['California', 'Ohio', 'Oregon', 'Texas']
    ser2 = Series(dict_data, index=states)
    ser3 = ser1 + ser2
    print('series1 + series2:\n', ser3)

    ser3.index.name = 'state'
    ser3.name = 'population'
    print('series with name:\n', ser3)


def pandas_df_demo01():
    # create df
    data_dict = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9],
    }
    print('dataframe:\n', DataFrame(data_dict))

    cols = ['year', 'state', 'pop']
    print('dataframe by year:\n', DataFrame(data_dict, columns=cols))
    idx = ['one', 'two', 'three', 'four', 'five']
    print('dataframe by index:\n', DataFrame(data_dict, index=idx))


def pandas_df_demo02():
    # create df
    data_dict = {
        'Nevada': {2001: 2.4, 2002: 2.9},
        'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6},
    }
    print('dataframe:\n', DataFrame(data_dict))

    idx = [2002, 2001, 2000]
    df = DataFrame(data_dict, index=idx)
    print('dataframe by index:\n', df)

    df.columns.name = 'state'
    df.index.name = 'year'
    print('dataframe by col and index:\n', df)


def pandas_df_demo03():
    # get df cols
    data_dict = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9],
    }
    df1 = DataFrame(data_dict)
    print('dataframe state:\n', df1['state'])
    print('dataframe population:\n', df1.year)

    # get df rows
    idx = ['one', 'two', 'three', 'four', 'five']
    df2 = DataFrame(data_dict, index=idx)
    print('dataframe row "one":\n', df2.loc['one'])
    print('dataframe row 2:\n', df2.iloc[1])

    rows = ['two', 'three', 'four']
    print('dataframe rows "two", "three", "four":\n', df2.loc[rows])
    print('dataframe row 1~3:\n', df2.iloc[range(3)])


def pandas_df_demo04():
    # get df field
    data_dict = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9],
    }
    idx = ['one', 'two', 'three', 'four', 'five']
    df = DataFrame(data_dict, index=idx)
    print('dataframe:\n', df)

    # index by [col,row]
    print('dataframe row 1 state:', df['state'][0])
    print('dataframe row two pop:', df['pop']['two'])
    # index by [row, col]
    print('dataframe row 1 state:', df.iloc[0]['state'])
    print('dataframe row two pop:', df.loc['two']['pop'])


def pandas_df_demo05():
    # update df
    data_dict = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9],
    }
    idx = ['one', 'two', 'three', 'four', 'five']
    df = DataFrame(data_dict, index=idx)

    df['debt'] = 10
    print('add col debt dataframe:\n', df)
    df1['debt'] = np.arange(5)
    print('update col debt dataframe:\n', df)

    east = (df['state'] == 'Ohio')
    df1['east'] = east
    print('add col east dataframe:\n', df)


def pandas_df_demo06():
    # 1
    df = DataFrame(np.arange(9).reshape(3, 3),
                   index=['bj', 'sh', 'gz'], columns=['a', 'b', 'c'])
    print('dataframe:\n', df)

    df.index = Series(['beijing', 'shanghai', 'guangzhou'])
    print('update index df:\n', df)
    df.index = df.index.map(str.upper)
    print('update index with upper df:\n', df)

    df1 = df.rename(index=str.lower, columns=str.upper)
    print('update index and cols df:\n', df1)

    # 2
    df2 = DataFrame([
        [2.0, 1.0, 3.0, 5],
        [3.0, 4.0, 5.0, 5],
        [3.0, 4.0, 5.0, 5],
        [1.0, 0.0, 6.0, 5]],
        columns=list('abcd'))
    print('sum by rows df:\n', df2.cumsum(axis=0))  # default
    print('sum by cols df:\n', df2.cumsum(axis=1))


def pandas_df_demo07():
    # function: pd.cut()
    np.random.seed(666)

    # 1
    score_list = np.random.randint(25, 100, size=20)
    print('scores:', score_list)

    partitions = [0, 59, 70, 80, 100]
    labels = ['low', 'middle', 'good', 'perfect']
    score_cut = pd.cut(score_list, partitions, labels=labels)
    print('category scores:\n', score_cut)
    print('category count:\n', pd.value_counts(score_cut))

    # 2
    df = DataFrame()
    df['score'] = score_list
    df['student'] = [pd.util.testing.rands(3) for i in range(len(score_list))]
    print('students and scores df:\n', df)

    df['category'] = pd.cut(df['score'], partitions, labels=labels)
    print('students and scores by category df:\n', df)

    # save to csv
    df.index.name = 'idx'
    save_path = os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files', 'test.out')
    df.to_csv(save_path)


def pandas_df_demo08():
    # np.dtype高效地存储数据
    mem = pd.DataFrame([[133, 2, 4]], columns=[
                       'uid', 'dogs', 'cats']).memory_usage()
    print('default int64 memory usage:\n', mem)

    mem = pd.DataFrame([[133, 2, 4]], columns=['uid', 'dogs', 'cats']) \
        .astype({
            'uid': np.dtype('int32'),
            'dogs': np.dtype('int32'),
            'cats': np.dtype('int32')
        }).memory_usage()
    print('\ndefault int32 memory usage:\n', mem)


def pandas_df_demo09():
    # axis=0 沿着行方向（纵向）, axis=1 沿着列方向（横向）
    df = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': [1, 2, 3],
        'col3': [1, 2, 3],
    })
    print('df data:\n', df)

    df1 = df.drop('col2', axis=1)
    print('\ndrop col2, and df data:\n', df1)
    df2 = df.drop(1, axis=0)
    print('\ndrop row2, and df data:\n', df2)

    avg1 = df.mean(axis=1)
    print('\navg value for each line:\n', avg1)
    avg2 = df.mean(axis=0)
    print('\navg value for each row:\n', avg2)


def pandas_plot_demo01():
    # series.plot()
    np.random.seed(666)
    s1 = Series(np.random.randn(1000)).cumsum()
    s2 = Series(np.random.randn(1000)).cumsum()

    show_num = 3
    if show_num == 1:
        s1.plot(kind='line', grid=True, label='S1', title='series_s1')
        s2.plot(label='s2')
    elif show_num == 2:
        figure, ax = plt.subplots(2, 1)
        ax[0].plot(s1)
        ax[1].plot(s2)
    elif show_num == 3:
        fig, ax = plt.subplots(2, 1)
        s1.plot(ax=ax[1], label='s1')
        s2.plot(ax=ax[0], label='s2')
    else:
        raise KeyError('invalid show_num!')

    plt.legend()
    plt.show()


def pandas_plot_demo02():
    # dataframe.plot()
    np.random.seed(666)
    df = DataFrame(np.random.randint(1, 20, size=40).reshape(10, 4),
                   columns=['a', 'b', 'c', 'd'])

    show_num = 3
    if show_num == 1:
        # 柱状图
        df.plot(kind='bar')
    elif show_num == 2:
        # 横向的柱状图
        df.plot(kind='barh')
    elif show_num == 3:
        for i in df.index:
            df.iloc[i].plot(label='row' + str(i))
        plt.legend()
    else:
        raise KeyError('invalid show_num!')

    plt.show()


def pandas_df_save_demo():
    data_dict = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9],
    }
    dir_path = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files')

    # save as csv
    df1 = DataFrame(data_dict, index=range(1, 6))
    print('dataframe to be saved as csv:\n', df1)
    df1.to_csv(os.path.join(dir_path, 'test_df.csv'))

    # save as parquet
    # pre-condition: pip3 install fastparquet
    pd.show_versions()

    df2 = DataFrame(data_dict)
    print('\ndataframe to be saved as parquet:\n', df2)
    # df2.to_parquet(os.path.join(dir_path, 'test_df.parquet.gzip'))
    # RuntimeError: Compression 'snappy' not available. Options: ['GZIP', 'UNCOMPRESSED']
    df2.to_parquet(os.path.join(dir_path, 'test_df.parquet.gzip'),
                   engine='fastparquet', compression='gzip')


def pandas_df_read_demo():
    home_dir = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files')

    # read csv
    csv_path = os.path.join(home_dir, 'test_df.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, index_col=0)
        print('read from csv, dataframe:\n', df)

    # read parquet
    file_path = os.path.join(home_dir, 'test_df.parquet.gzip')
    if os.path.exists(file_path):
        df = pd.read_parquet(file_path, engine='fastparquet')
        print('read from parquet, dataframe:\n', df)

    # read parquet(hive)
    file_path = os.path.join('/tmp/hive_test', 'pokes_0.parquet')
    if os.path.exists(file_path):
        limit = 11
        df = pd.read_parquet(file_path, engine='fastparquet')
        print('read from parquet(hive), dataframe:\n', df[:limit])


def pandas_read_excel_demo_01():
    file_path = get_lemon_cases_excel_path()
    df = pd.read_excel(file_path, sheet_name='multiply')

    # 按列读取数据
    # 返回一个Series对象，title列的数据
    print('col [title] as series:\n', df['title'])

    print('\ncol [title] list:', list(df['title']))
    print('col [df.title] list:', list(df.title))
    print('col [title] tuple:', tuple(df['title']))
    print('cols [index,title] dict:', dict(df['title']))  # key为数字索引

    print('\ncol [title] 1st value:', df['title'][0])

    print('\ncols [title,actual]:\n', df[['title', 'actual']])

    # 按行读取数据
    print('\nrow 1 (list):', list(df.iloc[0]))
    print('row 1 (tuple):', tuple(df.iloc[0]))
    print('row 1 (dict):', dict(df.iloc[0]))
    print('row last (dict):', dict(df.iloc[-1]))

    print('\nrow 1 [l_data]:', df.iloc[0]['l_data'])
    print('row 1 [l_data] by index:', df.iloc[0][2])

    print('\nrow 0-2:\n', df.iloc[0:3])

    # 读取所有数据
    print('\nall rows (dataframe):\n', df)
    print('\nall rows (list):\n', df.values)

    data_list = []
    for idx in df.index:
        data_list.append(df.iloc[idx].to_dict())
    print('\nall rows (list of dict):\n', data_list)


def pandas_read_excel_demo_02():
    file_path = get_lemon_cases_excel_path()
    df = pd.read_excel(file_path, sheet_name='multiply')

    # iloc, by index
    print('col 1 [index,case_id]:\n', df.iloc[:, 0])
    print('\ncol last [index,result]:\n', df.iloc[:, -1])
    print('\ncols 0-2 [index,case_id,title,l_data]:\n', df.iloc[:, 0:3])

    print('\n2-3 rows and 1-3 cols:\n', df.iloc[2:4, 1:4])
    print('\n1,3 rows and 2,4 cols:\n', df.iloc[[1, 3], [2, 4]])

    # loc, by name
    print('\n1-2 rows and col [title]:\n', df.loc[1:2, 'title'])
    print('\n1-2 rows and cols [title,l_data,r_data]:\n',
          df.loc[1:2, 'title':'r_data'])

    print('\ncols boolean(r_data > 5):\n', df['r_data'] > 5)
    print('\nrows (r_data > 5):\n', df.loc[df['r_data'] > 5])
    print('\nrows (r_data > 5) and cols [r_data,expected,actual]:\n',
          df.loc[df['r_data'] > 5, 'r_data':'actual'])


def pandas_write_excel_demo():
    file_path = get_lemon_cases_excel_path()
    df = pd.read_excel(file_path, sheet_name='multiply')

    df['result'][0] = 'test'
    output_path = os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files', 'lemon_cases_new.xlsx')
    # pip3 install openpyxl
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, sheet_name='new', index=False)


def get_lemon_cases_excel_path():
    file_path = os.path.join(
        os.getenv('PYPATH'), 'pydemos', 'data', 'lemon_cases.xlsx')
    if not os.path.exists(file_path):
        raise FileNotFoundError('file not found: ' + file_path)
    return file_path


def pandas_read_csv_demo():
    file_path = os.path.join(
        os.getenv('PYPATH'), 'pydemos', 'data', 'data.log')
    if not os.path.exists(file_path):
        raise FileNotFoundError('file not found: ' + file_path)

    # csv_frame = pd.read_csv(file_path)
    # csv_frame = pd.read_csv(file_path, header=None, names=['Col1', 'Col2', 'Col3'])
    df = pd.read_csv(file_path, sep=',')
    success_df = df.loc[df['Success'] == 0]
    testtime_series = success_df['TestTime']
    print('Success TestTime Series:\n', testtime_series)

    avg_result = round(sum(testtime_series) / len(testtime_series), 2)
    print('\nmin TestTime: %r, max TestTime: %r, avg TestTime: %r'
          % (min(testtime_series), max(testtime_series), avg_result))


if __name__ == '__main__':

    # pandas_series_demo02()
    pandas_df_demo09()

    # pandas_plot_demo02()

    # pandas_df_save_demo()
    # pandas_df_read_demo()

    # pandas_read_excel_demo_01()
    # pandas_read_excel_demo_02()
    # pandas_write_excel_demo()
    # pandas_read_csv_demo()

    print('pandas demo DONE.')
