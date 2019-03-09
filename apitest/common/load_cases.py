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

    __file_path = ''
    __load = None
    __test_cases = []

    @classmethod
    def get_instance(cls):
        if cls.__load is None:
            cls.__load = LoadCases()
        return cls.__load

    @classmethod
    def build(cls, file_path):
        cls.__file_path = file_path
        return cls

    def __init__(self):
        self.__logger = LogManager.get_instance().get_logger()
        self.__xlsx = XlsxUtils.get_instance()

    # --------------------------------------------------------------
    # Load test cases data
    # --------------------------------------------------------------
    def load_all_cases(self):
        sheets = self.__xlsx.get_sheets_names(self.__file_path)
        ret_tc = []
        for sheet in sheets:
            tmp_tcs = self.load_all_cases_by_sheet(sheet)
            ret_tc.extend(tmp_tcs)

        self.__test_cases = ret_tc
        return ret_tc

    def load_all_cases_by_sheet(self, sheet_name):
        sheet = self.__xlsx.load_sheet_data(self.__file_path, sheet_name)
        self.__test_cases = sheet.read_all_rows_by_sheet()
        return self.__test_cases

    def load_cases_by_sheet_and_tags(self, sheet_name, tags):
        '''
        tags: list of keywords, like ['p1', 'smoke']
        '''
        sheet = self.__xlsx.load_sheet_data(self.__file_path, sheet_name)
        tcs = sheet.read_all_rows()

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
        sheet = self.__xlsx.load_sheet_data(self.__file_path, sheet_name)
        tcs = sheet.read_all_rows()

        ret_tcs = []
        for tc in tcs:
            if tc[1] in ids:
                ret_tcs.append(tc)

        self.__test_cases = ret_tcs
        return ret_tcs

    # --------------------------------------------------------------
    # Get test cases data
    # --------------------------------------------------------------
    def get_loaded_tcs(self):
        return self.__test_cases

    def get_tc_data_dict(self, case_name):
        if len(self.__test_cases) == 0:
            raise Exception('Pls load test cases data first!')

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

    log_manager = LogManager.biuld(Constants.LOG_FILE_PATH).get_instance()
    file_path = os.path.join(os.path.dirname(os.getcwd()), 'TestCases.xlsx')
    load_cases = LoadCases.build(file_path).get_instance()
    
    sheet_name = 'Module01'
    # load_cases.load_all_cases_by_sheet(sheet_name)
    # load_cases.load_cases_by_ids(['test_index_get_01'])
    # load_cases.load_cases_by_sheet_and_tags(sheet_name, ['p1','smoke'])
    load_cases.load_all_cases()
    print(load_cases.get_loaded_tcs())
    print(load_cases.get_tc_data_dict('test_index_get_01'))

    log_manager.clear_log_handles()
    print('load test cases DONE.')
