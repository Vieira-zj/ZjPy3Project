# -*- coding: utf-8 -*-
'''
Created on 2019-03-08

@author: zhengjin
'''

import json
import sys
import os
import allure
import pytest

sys.path.append(os.getenv('PYPATH'))
from utils import Constants
from utils import LogManager
from utils import HttpUtils
from apitest.common import LoadCases
from apitest.testcases.test_base import TestBase


@allure.feature('MockTest')
@allure.story('Story_IndexPage')
class TestModule01(TestBase):

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

    def test_index_get_01(self):
        case = LoadCases.get_instance().get_tc_data_dict(self.__cur_case)
        headers = LoadCases.format_headers_to_dict(case[self.CASE_SCHEMA_HEADER])
        resp = self.__http_utils.send_http_request(
            case[self.CASE_SCHEMA_METHOD], case[self.CASE_SCHEMA_URL],
            case[self.CASE_SCHEMA_QUERY], headers=headers)
        # assert(resp is not None and resp.status_code == int(case['RetCode']))
        self.base_http_assert(resp)

    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    def test_index_get_02(self):
        case = LoadCases.get_instance().get_tc_data_dict(self.__cur_case)
        headers = LoadCases.format_headers_to_dict(case[self.CASE_SCHEMA_HEADER])
        resp = self.__http_utils.send_http_request(
            case[self.CASE_SCHEMA_METHOD], case[self.CASE_SCHEMA_URL],
            case[self.CASE_SCHEMA_QUERY], headers=headers)
        # assert(resp is not None and resp.status_code == int(case['RetCode']))
        self.base_http_assert(resp)

        ret_ok = resp.json()['results']
        expected_ok = json.loads(case[self.CASE_SCHEMA_EXP_MSG])['results']
        assert(ret_ok == expected_ok)

    def test_index_post_01(self):
        case = LoadCases.get_instance().get_tc_data_dict(self.__cur_case)
        headers = LoadCases.format_headers_to_dict(case[self.CASE_SCHEMA_HEADER])
        resp = self.__http_utils.send_http_request(
            case[self.CASE_SCHEMA_METHOD], case[self.CASE_SCHEMA_URL],
            case[self.CASE_SCHEMA_BODY], headers=headers)
        # assert(resp is not None and resp.status_code == int(case['RetCode']))
        self.base_http_assert(resp)


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)
    file_path = os.path.join(os.path.dirname(os.getcwd()), 'TestCases.xlsx')
    LoadCases.get_instance().pre_load_sheet(file_path, 'Module01').load_all_cases_by_sheet()

    pytest.main(['-v', '-s', 'test_module_01.py'])

    LogManager.clear_log_handles()
    print('test module 01 DONE.')
