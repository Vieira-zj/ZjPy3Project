# -*- coding: utf-8 -*-
'''
Created on 2018-10-30
@author: zhengjin

Includes unit test and selenium web ui test demo by "unittest" module.
'''

import chromedriver_binary
import os
import threading
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait

# --------------------------------------------------------------
# Unit Test
# --------------------------------------------------------------


class TestPy01(unittest.TestCase):
    '''
    unit test.
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
        self.assertTrue(re.search(
            'unknown|offline', test_str), 'search success')
        self.assertFalse(re.search(
            'unknown|online', test_str), 'search failed')

# --------------------------------------------------------------
# Web UI Test
# --------------------------------------------------------------


class TestPy02(unittest.TestCase):
    '''
    selenium web ui test.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.utils = TestUtils()
        self.ms_bing_page = MsBingPage()

    def test_selenium_chrome(self):
        '''
        selenium ui test with headless mode in local (chrome).

        pre-condition:
        pip3 install chromedriver-binary
        '''
        caps = {
            'browserName': 'chrome',
            'version': '',
            'platform': 'MAC',
            'javascriptEnabled': True,
        }
        br_options = ChromeOptions()
        br_options.add_argument('--headless')
        br_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(
            desired_capabilities=caps, options=br_options)
        browser.implicitly_wait(8)

        print('\nbrowser: %s, version: %s' % (
            browser.capabilities['browserName'], browser.capabilities['browserVersion']))
        try:
            self.ms_bing_page.open_steps(self, browser)
        finally:
            browser.quit()

    def test_selenium_grid_headless_chrome(self):
        '''
        selenium ui test with headless mode by grid, and vnc record is disabled (chrome).

        pre-condition: selenium grid is running.
        check selenium hub: curl "http://localhost:4444/wd/hub/status" | jq .
        '''
        br_options = ChromeOptions()
        br_options.add_argument('--headless')
        br_options.add_argument('--disable-gpu')

        caps = DesiredCapabilities.CHROME
        caps['platform'] = 'ANY'
        caps.update(br_options.to_capabilities())

        hub_url = 'http://localhost:4444/wd/hub'
        browser = webdriver.Remote(
            command_executor=hub_url, desired_capabilities=caps)
        browser.implicitly_wait(8)

        b_caps = browser.capabilities
        print('\nbrowser: %s, version: %s' %
              (b_caps.get('browserName', 'null'), b_caps.get('version', 'null')))
        try:
            self.ms_bing_page.open_steps(self, browser)
            self.utils.save_screenshot(browser, '/tmp/uitest_bing_home_01.png')
            self.ms_bing_page.search_steps(self, browser)
            self.utils.save_screenshot(
                browser, '/tmp/uitest_bing_search_01.png')
        finally:
            browser.quit()

    def test_selenium_grid_headless_firefox(self):
        '''
        selenium ui test with headless mode by grid, and vnc record is disabled (firefox).

        pre-condition: selenium grid is running.
        check selenium hub: curl "http://localhost:4444/wd/hub/status" | jq .
        '''
        br_options = FirefoxOptions()
        br_options.headless = True

        caps = DesiredCapabilities.FIREFOX
        caps['platform'] = 'ANY'
        caps.update(br_options.to_capabilities())

        hub_url = 'http://localhost:4444/wd/hub'
        browser = webdriver.Remote(
            command_executor=hub_url, desired_capabilities=caps)
        browser.implicitly_wait(8)

        b_caps = browser.capabilities
        print('\nbrowser: %s, version: %s' %
              (b_caps.get('browserName', 'unknown'), b_caps.get('version', 'unknown')))
        try:
            self.ms_bing_page.open_steps(self, browser)
            self.utils.save_screenshot(browser, '/tmp/uitest_bing_home_02.png')
            self.ms_bing_page.search_steps(self, browser)
            self.utils.save_screenshot(
                browser, '/tmp/uitest_bing_search_02.png')
        finally:
            browser.quit()

    def test_selenium_grid_vnc_debug(self):
        '''
        selenium ui test by grid, and vnc record is enabled (chrome).

        pre-condition: selenium grid is running.
        check selenium hub: curl "http://localhost:4444/wd/hub/status" | jq .
        '''
        caps = DesiredCapabilities.CHROME
        caps['platform'] = 'ANY'

        hub_url = 'http://localhost:4444/wd/hub'
        browser = webdriver.Remote(
            command_executor=hub_url, desired_capabilities=caps)
        browser.implicitly_wait(8)

        b_caps = browser.capabilities
        print('\nbrowser: %s, version: %s' %
              (b_caps.get('version', 'unknown'), b_caps.get('browserName', 'unknown')))
        try:
            self.ms_bing_page.open_steps(self, browser)
            self.ms_bing_page.search_steps(self, browser)
        finally:
            browser.quit()

# --------------------------------------------------------------
# UI Test Steps
# --------------------------------------------------------------


class MsBingPage(object):
    '''
    ms bing search home page.
    '''

    def open_steps(self, t, browser):
        open_url = 'https://cn.bing.com/'
        browser.get(open_url)
        print('page title:', browser.title)
        t.assertTrue('Bing' in browser.title, 'verify ms bing page title')

        en_tab = WebDriverWait(browser, 5, 0.5).until(
            cond.presence_of_element_located((By.ID, 'est_en')))
        print('en tab element text:', en_tab.text)
        t.assertTrue('国际版' in en_tab.text, 'verify en tab element text')
        en_tab.click()
        time.sleep(1)

    def search_steps(self, t, browser):
        input = browser.find_element_by_id('sb_form_q')
        t.assertIsNotNone(input, 'verify input element is exist')
        input.send_keys('docker selenium')
        input.submit()
        time.sleep(2)


class TestUtils(object):
    '''
    test utils.
    '''

    def __init__(self):
        self.is_screenshot = False

    def save_screenshot(self, browser, path):
        if not self.is_screenshot:
            return

        if os.path.exists(path):
            os.remove(path)
        browser.save_screenshot(path)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    # unittest.main(verbosity=2)

    tests = []
    # tests.append(TestPy01('test_subprocess'))
    tests.append(TestPy01('test_time_counter'))
    # tests.append(TestPy01('test_reg_expr'))

    # selenium test
    # tests.append(TestPy02('test_selenium_chrome'))
    # tests.append(TestPy02('test_selenium_grid_headless_chrome'))
    # tests.append(TestPy02('test_selenium_grid_headless_firefox'))
    # tests.append(TestPy02('test_selenium_grid_vnc_debug'))

    suite = unittest.TestSuite()
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
