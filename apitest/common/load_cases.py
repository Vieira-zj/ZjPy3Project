# -*- coding: utf-8 -*-
'''
Created on 2019-03-06

@author: zhengjin
'''

import sys
import os

sys.path.append('../../')
from utils import Constants
from utils import LogManager 
from utils import XlsxUtils


class LoadCases(object):

    __load = None

    @classmethod
    def get_instance(cls):
        if cls.__load is None:
            cls.__load = LoadCases()
        return cls.__load

    def __init__(self):
        self.__logger = LogManager.get_logger()
        self.__xlsx = XlsxUtils.get_instance()
        self.__test_cases = []

    # --------------------------------------------------------------
    # Load test cases data
    # --------------------------------------------------------------
    def load_all_cases(self, file_path):
        sheets = self.__xlsx.get_all_sheets_names(file_path)
        
        ret_tc = []
        for sheet in sheets:
            tmp_tcs = self.pre_load(file_path, sheet).load_all_cases_by_sheet()
            ret_tc.extend(tmp_tcs)

        self.__test_cases = ret_tc
        return ret_tc

    def pre_load(self, file_path, sheet_name):
        self.__xlsx.load_sheet_data(file_path, sheet_name)
        return self

    def load_all_cases_by_sheet(self):
        self.__test_cases = self.__xlsx.read_all_rows_by_sheet()
        return self.__test_cases

    def load_cases_by_sheet_and_tags(self, tags):
        '''
        tags: list of keywords, like ['p1', 'smoke']
        '''
        tcs = self.__xlsx.read_all_rows_by_sheet()
        ret_tcs = []
        for tc in tcs:
            tmp_tags = tc[2].split(',')
            found = True
            for tag in tags:
                if tag not in tmp_tags:
                    found = False
                    break
            if found:
                ret_tcs.append(tc)

        self.__test_cases = ret_tcs
        return ret_tcs

    def load_cases_by_ids(self, ids):
        tcs = self.__xlsx.read_all_rows_by_sheet()

        ret_tcs = []
        for tc in tcs:
            if tc[1] in ids:
                ret_tcs.append(tc)

        self.__test_cases = ret_tcs
        return ret_tcs

    def get_loaded_tcs(self):
        return self.__test_cases

    # --------------------------------------------------------------
    # Get test case data
    # --------------------------------------------------------------
    def get_tc_data_dict(self, case_name):
        if len(self.__test_cases) == 0:
            raise Exception('No test cases found!')

        headers = self.__xlsx.read_header_row()
        if len(headers) == 0:
            raise Exception('No header defined for test case!')

        case = []
        for tc in self.get_loaded_tcs():
            if tc[1] == case_name:
                case = tc

        ret_dict = {}
        for k, v in zip(headers, case):
            ret_dict[k] = v
        return ret_dict

    # --------------------------------------------------------------
    # Format case fields
    # --------------------------------------------------------------
    @classmethod
    def format_headers_to_dict(cls, headers_str):
        ret_dict = {}
        headers = headers_str.split(',')
        for header in headers:
            if header.find(':') == -1:
                break
            fields = header.split(':')
            ret_dict[fields[0]] = fields[1]

        return ret_dict


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)

    file_path = os.path.join(os.path.dirname(os.getcwd()), 'TestCases.xlsx')
    LoadCases.get_instance().load_all_cases(file_path)
    print(LoadCases.get_instance().get_loaded_tcs())

    sheet_name = 'Module01'
    load_cases = LoadCases.get_instance().pre_load(file_path, sheet_name)
    # load_cases.load_all_cases_by_sheet()
    # load_cases.load_cases_by_ids(['test_index_get_01'])
    load_cases.load_cases_by_sheet_and_tags(['p1','smoke'])
    print(load_cases.get_loaded_tcs())
    
    print(load_cases.get_tc_data_dict('test_index_get_01'))

    LogManager.clear_log_handles()
    print('load test cases DONE.')
