# -*- coding: utf-8 -*-
'''
Created on 2019-05-26
@author: zhengjin
'''

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
    print('series item at "a":', ser['a'])
    print('series item at "a" and "c":\n', ser[['a', 'c']])

    print('series index:\n', ser.index)
    print('series values:\n', ser.values)


def pandas_series_demo03():
    # operation on series
    ser = Series(range(4), index=['a', 'b', 'c', 'd'])
    print('series, items > 2:\n', ser[ser > 1])
    print('series, items * 2:\n', ser * 2)
    print('square series:\n', np.square(ser))

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
    print('dataframe by index:', df)

    # set col and index name
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
    pass


if __name__ == '__main__':

    # pandas_series_demo03()
    pandas_df_demo04()
    print('pandas demo DONE.')
