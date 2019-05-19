# -*- coding: utf-8 -*-
'''
Created on 2019-05-18
@author: zhengjin
'''

import tensorflow as tf
import numpy as np
import os


def logistic_regression():
    # 输入数据
    x_data = np.linspace(-1, 1, 300)[:, np.newaxis]
    noise = np.random.normal(0, 0.05, x_data.shape)
    y_data = np.square(x_data)-0.5+noise

    # 输入层（1个神经元）
    xs = tf.placeholder(tf.float32, [None, 1])
    ys = tf.placeholder(tf.float32, [None, 1])

    # 隐层（10个神经元）
    W1 = tf.Variable(tf.random_normal([1, 10]))
    b1 = tf.Variable(tf.zeros([1, 10])+0.1)
    Wx_plus_b1 = tf.matmul(xs, W1) + b1
    # 激活函数tf.nn.relu
    tmp_ys = tf.nn.relu(Wx_plus_b1)

    # 输出层（1个神经元）
    W2 = tf.Variable(tf.random_normal([10, 1]))
    b2 = tf.Variable(tf.zeros([1, 1])+0.1)
    Wx_plus_b2 = tf.matmul(tmp_ys, W2) + b2
    ys_ = Wx_plus_b2

    # 损失和训练
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-ys_), reduction_indices=[1]))
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    # run session
    saver = tf.train.Saver()
    model_dir = '/tf/tf_scripts/model'

    with tf.Session() as sess:
        if os.path.exists(os.path.join(model_dir, 'checkpoint')):
            print('session restore from model checkpoint.')
            saver.restore(sess, os.path.join(model_dir, 'model.ckpt'))
        else:
            print('run session from init.')
            init = tf.global_variables_initializer()
            sess.run(init)

        # 训练1000次
        for i in range(1000):
            feed_dict = {xs: x_data, ys: y_data}
            _, loss_val = sess.run([train_step, loss], feed_dict=feed_dict)

            if(i % 50 == 0):
                print('loss:', loss_val)
                save_path = saver.save(sess, os.path.join(model_dir, 'model.ckpt'))
# logistic_regression


if __name__ == '__main__':

    logistic_regression()
    print('tensorflow linear expression DONE!')
