# -*- coding: utf-8 -*-
'''
Created on 2018-10-30

@author: zhengjin
'''

import threading
import time
import unittest


class Test(unittest.TestCase):

    def test01_threads(self):

        def sub_process():
            for i in range(3):
                print('test and wait at %d' % i)
                time.sleep(1)

        t = threading.Thread(target=sub_process)
        t.start()
        print('in main thread and wait\n')
        t.join()

    def test02_time(self):
        now = time.perf_counter()
        time.sleep(3)
        during = time.perf_counter() - now
        print('during %d' % during)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
