# -*- coding: utf-8 -*-
'''
Created on 2019-03-10

@author: zhengjin
'''

import sys
import os
import pytest

sys.path.append('../../')
from utils import Constants
from utils import LogManager
from utils import HttpUtils
from apitest.common import LoadCases


class TestModule02(object):

    __logger = None
    __http_utils = None

    def setup_class(cls):
        cls.__logger = LogManager.get_logger()
        cls.__http_utils = HttpUtils.get_instance()

    def teardown_class(cls):
        pass

    def setup_method(self, method):
        self.__cur_case = method.__name__

    def teardown_method(self, method):
        pass

    def test_error_get_01(self):
        case = LoadCases.get_instance().get_tc_data_dict(self.__cur_case)
        headers = LoadCases.format_headers_to_dict(case['Headers'])
        resp = self.__http_utils.send_http_request(
            case['Method'], case['Url'], case['Query'], headers=headers)
        assert(resp is not None and resp.status_code == int(case['RetCode']))

    def test_error_get_02(self):
        case = LoadCases.get_instance().get_tc_data_dict(self.__cur_case)
        headers = LoadCases.format_headers_to_dict(case['Headers'])
        resp = self.__http_utils.send_http_request(
            case['Method'], case['Url'], case['Query'], headers=headers)
        assert(resp is not None and resp.status_code == int(case['RetCode']))

    def test_error_get_03(self):
        case = LoadCases.get_instance().get_tc_data_dict(self.__cur_case)
        headers = LoadCases.format_headers_to_dict(case['Headers'])
        resp = self.__http_utils.send_http_request(
            case['Method'], case['Url'], case['Query'], headers=headers)
        assert(resp is not None and resp.status_code == int(case['RetCode']))


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)
    file_path = os.path.join(os.path.dirname(os.getcwd()), 'TestCases.xlsx')
    LoadCases.get_instance().pre_load_sheet(
        file_path, 'Module02').load_all_cases_by_sheet()

    pytest.main(['-v', '-s', 'test_module_02.py'])

    LogManager.clear_log_handles()
    print('test module 02 DONE.')
