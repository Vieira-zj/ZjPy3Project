# -*- coding: utf-8 -*-
'''
Created on 2019-05-18
@author: zhengjin

tensorflow board web:
$ tensorboard --logdir /tf/notebooks/logs
'''

import tensorflow as tf
import os


def tensorflow_world():
    welcome = tf.constant('Welcome to TensorFlow world!')
    # run the session
    with tf.Session() as sess:
        print('output:', sess.run(welcome))


def tensorflow_math_operations():
    FLAGS = tf.app.flags.FLAGS
    if not os.path.isabs(os.path.expanduser(FLAGS.log_dir)):
        raise ValueError('You must assign absolute path for log_dir')

    # define some constant values
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

    if writer is not None:
        writer.close()


if __name__ == '__main__':

    # logs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    logs_path = os.path.join(os.getcwd(), 'logs')
    print('events log path:', logs_path)
    desc = 'Directory where event logs are written to.'
    tf.app.flags.DEFINE_string('log_dir', logs_path, desc)

    # tensorflow_world()
    tensorflow_math_operations()

    print('tensorflow world DONE!')
