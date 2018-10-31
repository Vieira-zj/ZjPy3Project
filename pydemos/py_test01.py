# -*- coding: utf-8 -*-
'''
Created on 2018-10-30

@author: zhengjin
'''

import threading
import time
import unittest


class TestPy01(unittest.TestCase):
    '''
    unit test refer to:
    https://blog.csdn.net/xiaoquantouer/article/details/75089200
    '''

    def test_subprocess(self):

        def subprocess_main():
            for i in range(3):
                print('test and wait at %d' % i)
                time.sleep(1)

        t = threading.Thread(target=subprocess_main)
        t.start()
        print('in main thread and wait\n')
        t.join()

    def test_time_counter(self):
        now = time.perf_counter()
        time.sleep(3)
        during = time.perf_counter() - now
        print('during %.3f' % during)
        self.assertEqual(3, int(round(during)), 'test time counter')

    def test_reg_expr(self):
        import re
        test_str = 'list: device offline'
        self.assertTrue(re.search('unknown|offline', test_str), 'search success')
        self.assertFalse(re.search('unknown|online', test_str), 'search failed')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#     unittest.main(verbosity=2)
    
    suite = unittest.TestSuite()
    tests = []
#     tests.append(TestPy01('test_subprocess'))
#     tests.append(TestPy01('test_time_counter'))
    tests.append(TestPy01('test_reg_expr'))
    suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
