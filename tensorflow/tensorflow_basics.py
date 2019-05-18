# -*- coding: utf-8 -*-
'''
Created on 2019-05-18
@author: zhengjin

tensorflow board web:
$ tensorboard --logdir /home/tensorflow/logs
'''

from __future__ import print_function
from tensorflow_world import tensorflow_prepare
import tensorflow as tf
import os


def tensorflow_math_operations():
    tensorflow_prepare()
    FLAGS = tf.app.flags.FLAGS
    if not os.path.isabs(os.path.expanduser(FLAGS.log_dir)):
        raise ValueError('You must assign absolute path for log_dir')

    # defining some constant values
    a = tf.constant(5.0, name='a')
    b = tf.constant(10.0, name='b')

    # some basic operations
    x = tf.add(a, b, name='add')
    y = tf.div(a, b, name='divide')

    with tf.Session() as sess:
        writer = tf.summary.FileWriter(os.path.expanduser(FLAGS.log_dir), sess.graph)
        print("a =", sess.run(a))
        print("b =", sess.run(b))
        print("a + b =", sess.run(x))
        print("a/b =", sess.run(y))
        # print('output:', sess.run([a, b, x, y]))
        # output: [5.0, 10.0, 15.0, 0.5]

    writer.close()
    sess.close()


def tensorflow_variables():
    from tensorflow.python.framework import ops

    # defining Variables
    weights = tf.Variable(tf.random_normal([2, 3], stddev=0.1), name='weights')
    biases = tf.Variable(tf.zeros([3]), name='biases')
    custom_variable = tf.Variable(tf.zeros([3]), name='custom')

    # customized initializer
    variable_list_custom = [weights, custom_variable]
    init_custom_op = tf.variables_initializer(var_list=variable_list_custom)

    # global initializer #1
    init_all_op = tf.global_variables_initializer()

    # global initializer #2
    # all_variables_list = ops.get_collection(ops.GraphKeys.GLOBAL_VARIABLES)
    # init_all_op = tf.variables_initializer(var_list=all_variables_list)

    # initialization using other variables
    weights_new = tf.Variable(weights.initialized_value(), name='WeightsNew')
    init_weightsnew_op = tf.variables_initializer(var_list=[weights_new])

    # running the session
    with tf.Session() as sess:
        sess.run(init_all_op)
        sess.run(init_custom_op)
        sess.run(init_weightsnew_op)

    sess.close()


if __name__ == '__main__':

    tensorflow_math_operations()
    # tensorflow_variables()
    print('tensorflow basics DONE!')
