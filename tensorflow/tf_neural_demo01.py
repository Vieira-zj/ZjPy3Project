# -*- coding: utf-8 -*-
'''
Created on 2019-05-20
@author: zhengjin
'''

import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)


def tf_neural_network_raw():
    pass


if __name__ == '__main__':

    tf_neural_network_raw()
    print('tensorflow logistic expression DONE!')
