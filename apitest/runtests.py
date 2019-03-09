# -*- coding: utf-8 -*-
'''
Created on 2019-03-08

@author: zhengjin
'''

import pytest
import os
import sys

sys.path.append('../')
from utils import LogManager
from apitest.common import LoadConfigs


class RunTests(object):

    def __init__(self):
        log_path = os.path.join(os.getcwd(), 'outputs/logs')
        self.__log_manager = LogManager.build(log_path).get_instance()
        self.__logger =LogManager.get_logger()

    def setup_tests(self):
        self.__logger.info('INIT TESTS')
        cfg_file_path = os.path.join(os.getcwd(), 'configs.ini')
        LoadConfigs.load_configs(cfg_file_path)

    def tearup_tests(self):
        if self.__log_manager is not None:
            self.__log_manager.clear_log_handles()
        self.logger.info('END API TESTS')

    def run_tests(self):
        self.logger.info('START API TESTS')
        pass

if __name__ == '__main__':

    pytest.main(['-v', '-s', 'test_module_01.py'])
