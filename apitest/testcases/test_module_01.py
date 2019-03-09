# -*- coding: utf-8 -*-
'''
Created on 2019-03-08

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

class TestModule01(object):

    __logger = None
    __http_utils = None

    def setup_class(cls):
        cls.__logger = LogManager.get_instance().get_logger()
        cls.__http_utils = HttpUtils.get_instance()

    def teardown_class(cls):
        pass

    def setup_method(self, method):
        self.__cur_case = method.__name__

    def teardown_method(self, method):
        pass

    def test_index_get_01(self):
        case = LoadCases.get_instance().get_tc_data_dict(self.__cur_case)
        headers = LoadCases.format_headers_to_dict(case['Headers'])
        resp = self.__http_utils.send_http_request(
            HttpUtils.HTTP_METHOD_GET, case['Url'], case['Body'], headers=headers)
        assert(resp is not None and resp.status_code == 200)


if __name__ == '__main__':

    log_manager = LogManager.biuld(Constants.LOG_FILE_PATH).get_instance()
    file_path = os.path.join(os.path.dirname(os.getcwd()), 'TestCases.xlsx')
    LoadCases.build(file_path).get_instance().load_all_cases_by_sheet('Module01')

    pytest.main(['-v', '-s', 'test_module_01.py'])

    log_manager.clear_log_handles()
    print('test module 01 DONE.')
