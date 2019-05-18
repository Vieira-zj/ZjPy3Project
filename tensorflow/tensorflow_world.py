# -*- coding: utf-8 -*-
'''
Created on 2019-05-18
@author: zhengjin

tensorflow board web:
$ tensorboard --logdir /home/tensorflow/logs
'''

from __future__ import print_function
import tensorflow as tf
import os


def tensorflow_prepare():
    logs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    desc = 'Directory where event logs are written to.'
    tf.app.flags.DEFINE_string('log_dir', logs_path, desc)


def tensorflow_world():
    FLAGS = tf.app.flags.FLAGS
    if not os.path.isabs(os.path.expanduser(FLAGS.log_dir)):
        raise ValueError('You must assign absolute path for log_dir')

    # defining some sentence
    welcome = tf.constant('Welcome to TensorFlow world!')

    # run the session
    with tf.Session() as sess:
        writer = tf.summary.FileWriter(os.path.expanduser(FLAGS.log_dir), sess.graph)
        print('output:', sess.run(welcome))

    writer.close()
    sess.close()


if __name__ == '__main__':

    tensorflow_prepare()
    tensorflow_world()
    print('tensorflow world DONE!')
