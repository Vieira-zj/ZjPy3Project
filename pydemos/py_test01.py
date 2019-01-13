# -*- coding: utf-8 -*-
'''
Created on 2018-10-30
@author: zhengjin

Run test demos by using python "unittest" module.
'''

import threading
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait


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

    # --------------------------------------------------------------
    # Selenium grid demos
    # --------------------------------------------------------------
    def test_selenium_chrome(self):
        '''
        selenium headless demo in local (chrome).
        '''
        caps = {
            'browserName': 'chrome',
            'version': '',
            'platform': 'MAC',
            'javascriptEnabled': True,
        }

        # headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        DRIVER_PATH = '/Users/zhengjin/Downloads/selenium_driver/chromedriver'
        browser = webdriver.Chrome(
            executable_path=DRIVER_PATH, desired_capabilities=caps, chrome_options=chrome_options)
        browser.implicitly_wait(8)
        print('browser info:', browser.get('version', 'null'))

        open_url = 'http://www.baidu.com'
        browser.get(open_url)
        print('page title:', browser.title)
        self.assertTrue('百度' in browser.title, 'verify baidu page title')

        element = WebDriverWait(browser, 5, 0.5).until(cond.presence_of_element_located((By.ID, 'setf')))
        print('element text:', element.text)
        self.assertTrue('百度' in element.text, 'verify element text')

        time.sleep(1)
        browser.quit()

    def test_selenium_grid_debug(self):
        '''
        selenium grid debug, with vnc record enabled.
        grid in docker: $ docker-compose -f selenium-hub-compose-debug.yaml up
        '''
        # caps = DesiredCapabilities.CHROME
        caps = DesiredCapabilities.FIREFOX
        caps['platform'] = 'ANY'

        # check hub status:
        # http://localhost:4444/wd/hub/status
        hub_url = 'http://localhost:4444/wd/hub'

        browser = webdriver.Remote(command_executor=hub_url, desired_capabilities=caps)
        browser.implicitly_wait(8)
        print('browser info:', browser.capabilities.get('version', 'null'))

        open_url = 'http://www.baidu.com'
        browser.get(open_url)
        print('page title:', browser.title)
        self.assertTrue('百度' in browser.title, 'verify baidu page title')

        element = WebDriverWait(browser, 5, 0.5).until(
            cond.presence_of_element_located((By.ID, 'setf')))
        print('element text:', element.text)
        self.assertTrue('百度' in element.text, 'verify element text')

        time.sleep(1)
        browser.quit()

    def test_selenium_grid_headless(self):
        '''
        selenium grid with vnc record disabled for headless mode (chrome).
        grid in docker: $ docker-compose -f selenium-hub-compose.yaml up
        '''
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        caps = DesiredCapabilities.CHROME
        caps['platform'] = 'ANY'
        caps.update(chrome_options.to_capabilities())

        hub_url = 'http://localhost:4444/wd/hub'
        browser = webdriver.Remote(command_executor=hub_url, desired_capabilities=caps)
        browser.implicitly_wait(8)
        print('browser info:', browser.capabilities['version'])

        open_url = 'http://www.baidu.com'
        browser.get(open_url)
        print('page title:', browser.title)
        self.assertTrue('百度' in browser.title, 'verify baidu page title')

        element = WebDriverWait(browser, 5, 0.5).until(
            cond.presence_of_element_located((By.ID, 'setf')))
        print('element text:', element.text)
        self.assertTrue('百度' in element.text, 'verify element text')

        time.sleep(1)
        browser.quit()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    # unittest.main(verbosity=2)

    suite = unittest.TestSuite()
    tests = []
    # tests.append(TestPy01('test_subprocess'))
    tests.append(TestPy01('test_time_counter'))
    # tests.append(TestPy01('test_reg_expr'))

    # selenium test
    # tests.append(TestPy01('test_selenium_chrome'))
    # tests.append(TestPy01('test_selenium_grid_debug'))
    # tests.append(TestPy01('test_selenium_grid_headless'))

    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
