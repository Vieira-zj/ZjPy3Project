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

    def test_selenium_chrome(self):
        from selenium import webdriver

        open_url = 'http://www.baidu.com'
        chrome_driver = "/Users/zhengjin/Downloads/selenium_driver/chromedriver"

        browser = webdriver.Chrome(chrome_driver)
        browser.get(open_url)
        print('page title:', browser.title)

        browser.find_element_by_id('')

        time.sleep(1)
        browser.quit()

    def test_selenium_grid_chrome(self):
        from selenium import webdriver
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        open_url = 'http://www.baidu.com'
        hub_url = ''

        driver = webdriver.Remote(command_executor=hub_url, desired_capabilities=DesiredCapabilities.CHROME)
        driver.get(open_url)
        driver.find_element_by_id('')
        driver.close()

    def test_selenium_grid_any(self):
        # TODO:
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    # unittest.main(verbosity=2)

    suite = unittest.TestSuite()
    tests = []
    # tests.append(TestPy01('test_subprocess'))
    # tests.append(TestPy01('test_time_counter'))
    # tests.append(TestPy01('test_reg_expr'))
    
    # selenium test
    tests.append(TestPy01('test_selenium_chrome'))

    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
