# -*- coding: utf-8 -*-
'''
Created on 2019-01-08

@author: zhengjin
'''

import sys
import threading
import time

from kazoo.client import KazooClient
from kazoo.client import ChildrenWatch
from kazoo.client import DataWatch


def zk_test(zkc, zk_path):
    '''
    kazoo api reference:
    https://kazoo.readthedocs.io/en/latest/api/client.html
    '''
    def _data_change(event):
        print('watcher, node data changed.')
        print('event type %s, path %s' % (event.type, event.path))

    root_path = zk_path

    path_child_01 = '/child_01'
    child01 = zkc.create(root_path + path_child_01, b'py_zk_test_01')
    print('create node:', child01)

    path_child_02 = '/child_02'
    child02 = zkc.create(root_path + path_child_02,
                         b'py_zk_test_tmp_02', ephemeral=True)
    print('create temp node', child02)

    data, stat = zkc.get(root_path, watch=None)
    # data, stat = zkc.get(root_path, watch=_data_change)
    print('root node data:', data)
    print('root node state version:', stat.version)
    print('root node state length:', stat.data_length)
    print('root node children number:', stat.numChildren)

    stat = zkc.set(root_path, value=b'py_zk_test_root_modify')
    print('data updated, root node state version:', stat.version)

    if zkc.exists(root_path + path_child_01):
        if zkc.delete(root_path + path_child_01, recursive=False):
            print('delete node:', path_child_01)

    print('root node children:', zkc.get_children(root_path))


class zkWatcherTest(object):
    '''
    Watcher可以通过两种方式设置: 
    一种是在调用ZK客户端方法的时候传递进去, 比如 zk.get_children("/node", watch=FUN), 但是这种方法是一次性的, 
    也就是触发一次就没了, 如果你还想继续监听一个事件就需要再次注册.
    另外一种方法是通过高级API实现, 监控数据或者节点变化, 它只需要我们注册一次, 在Python里面就是kazoo. 
    高级API其实是对低级API的封装，对用户来讲更加好用。
    '''

    def __init__(self, zkc, zk_path):
        self._zk = zkc
        self._zk_path = zk_path

    def exec(self):
        ChildrenWatch(client=self._zk, path=self._zk_path,
                      func=self._node_change)
        DataWatch(client=self._zk, path=self._zk_path, func=self._data_change)
        print('zk watcher is running ...')
        time.sleep(6)

    def _node_change(self, children):
        print('watcher, children changed:', children)
        # TODO: print add, delete nodes

    def _data_change(self, data, stat):
        print('watcher, node data changed.')
        print('changed data:', data)
        print('state length:', stat.dataLength)
        print('state version:', stat.version)
        print('node children number:', stat.numChildren)


if __name__ == '__main__':

    url = '127.0.0.1:2181'
    zk_root_path = '/zk_test'
    zkc = KazooClient(hosts=url, timeout=100)
    zkc.start()

    try:
        if not zkc.exists(zk_root_path):
            zkc.create(zk_root_path, b'py_zk_test_root')

        is_watcher_set = True
        p = None
        if is_watcher_set:
            zk_watcher_test = zkWatcherTest(zkc, zk_root_path)
            p = threading.Thread(target=zk_watcher_test.exec)
            p.start()

        time.sleep(2)
        zk_test(zkc, zk_root_path)

        if p is not None:
            p.join()
    finally:
        zkc.stop()

    print('zookeeper test demo done.')
