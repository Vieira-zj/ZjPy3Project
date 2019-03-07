# -*- coding: utf-8 -*-
'''
Created on 2019-03-07

@author: zhengjin
'''

import os
import json
import sys
import xlrd

sys.path.append('../')
from utils import Constants
from utils import LogManager


class XlsxUtils(object):

    __utils = None

    @classmethod
    def get_instance(cls, logger, file_path, sheet_name, has_header_line=True):
        if cls.__utils is None:
            cls.__utils = XlsxUtils(logger, file_path, sheet_name, has_header_line)
        return cls.__utils

    def __init__(self, logger, file_path, sheet_name, has_header_line):
        if not os.path.exists(file_path):
            raise FileNotFoundError('Excel file is not exist: ' + file_path)

        self.__logger = logger
        self.__sheet = None
        self.__has_header_line = has_header_line

        self.load_sheet_data(file_path, sheet_name)

    def load_sheet_data(self, file_path, sheet_name, has_header_line=True):
        self.__logger.info('load file %s sheet %s' % (file_path, sheet_name))
        workbook = xlrd.open_workbook(file_path)
        self.__sheet = workbook.sheet_by_name(sheet_name)
        self.__has_header_line = has_header_line

    # --------------------------------------------------------------
    # Read data from excel sheet
    # --------------------------------------------------------------
    def read_all_rows(self):
        ret_rows = []
        for row in self.__sheet.get_rows():
            tmp_row = []
            for cell in row:
                tmp_row.append(str(cell.value))
            ret_rows.append(tmp_row)

        return ret_rows[1:] if self.__has_header_line else ret_rows

    def read_values_by_cloumn(self, col_num):
        ret_vals = []
        for row in self.__sheet.get_rows():
            ret_vals.append(row[col_num].value)

        return ret_vals[1:] if self.__has_header_line else ret_vals

    def read_cel_value(self, row_num, col_num):
        ret_val = self.__sheet.cell(row_num, col_num).value
        return str(ret_val)

    # --------------------------------------------------------------
    # Write data to excel sheet
    # --------------------------------------------------------------
    # TODO:


if __name__ == '__main__':

    file_path = os.path.join(os.path.dirname(os.getcwd()), 'apitest', 'TestCases.xlsx')
    sheet_name = 'Module01'

    log_manager = LogManager(Constants.LOG_FILE_PATH)
    xlsx = XlsxUtils.get_instance(log_manager.get_logger(), file_path, sheet_name)

    # excel cell index start with (0,0)
    # print(xlsx.read_all_rows())
    print('test cases:', xlsx.read_values_by_cloumn(1))
    print('1st case name:', xlsx.read_cel_value(1, 1))

    log_manager.clear_log_handles()
    print('xlsx utils test DONE.')
