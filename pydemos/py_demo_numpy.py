# -*- coding: utf-8 -*-
'''
Created on 2019-05-26
@author: zhengjin
'''

import numpy as np


def numpy_demo01():
    # create array
    arr1 = np.array([6, 7.5, 8, 0, 1])
    print('numpy 1d array:\n', arr1)

    arr2 = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    print('numpy 2d array:\n', arr2)
    print('array: type=%r, len=%d, shape=%r' % (arr2.dtype, arr2.ndim, arr2.shape))

    print('zeros array:\n', np.zeros(10))
    print('ones array:\n', np.ones((3, 5)))
    print('array by range:\n', np.arange(10))


def numpy_demo02():
    # array dtype
    arr1 = np.array([1, 2, 3, 4], dtype=np.float64)
    arr2 = np.array([4, 3, 2, 1], dtype=np.int32)
    print('arr1 type: %r, arr2 type: %r' % (arr1.dtype, arr2.dtype))
    print('float array:\n', arr1)
    print('int array:\n', arr2)

    arr3 = arr2.astype(np.float32)
    print('arr3 type:', arr3.dtype)


def numpy_demo03():
    # operation on array
    arr = np.array([[1., 2., 3.], [4., 5., 6.]])
    print('arr * arr:\n', arr * arr)
    print('arr * 0.5:\n', arr * 0.5)


def numpy_demo04():
    # index and slice
    arr = np.arange(10)
    print('arr element at 5:', arr[5])
    print('arr element at 5~8:', arr[5:8])

    # 和list类型有很大的不同的是，操作原数组的子序列的时候，实际上就是操作原数组的数据
    arr_slice = arr[:4]
    arr_slice[:] = 10
    print('arr slice:\n', arr_slice)
    print('src arr:\n', arr)

    # 复制操作
    arr_copy = arr[:3].copy()
    arr_copy[:] = 20
    print('arr copy:\n', arr_copy)
    print('src arr:\n', arr)


def numpy_demo05():
    # index for 2d array
    arr2d = np.arange(1, 10).reshape((3, 3))
    print('2d [3,3] arr:\n', arr2d)

    print('arr 1st row:', arr2d[0])
    print('arr element at [0,1]:', arr2d[0][1])
    print('arr element at [1,1]:', arr2d[1, 1])

    arr2d[0] = 10
    print('update arr:\n', arr2d)


def numpy_demo06():
    # array function
    arr1 = np.arange(10)
    print('sqrt arr:\n', np.sqrt(arr1))
    print('square arr:\n', np.square(arr1))

    arr2 = np.array([3, 3, 3, 2, 2, 1, 1, 4, 4])
    print('unique arr:\n', np.unique(arr2))

    arr3 = np.arange(32).reshape(8, 4)
    print('sum array:', arr3.sum())
    print('mean arr:', arr3.mean())
    print('mean for each row:\n', arr3.mean(axis=1))


def numpy_demo07():
    # create random array
    print('random arr:\n', np.random.normal(size=10))
    print('random int arr:\n', np.random.randint(1, high=100, size=10))
    print('random (0,1) arr:\n', np.random.uniform(size=10))


if __name__ == '__main__':

    numpy_demo07()
    print('numpy demo DONE.')
