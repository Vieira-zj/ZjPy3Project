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
    def get_instance(cls):
        if cls.__utils is None:
            logger = LogManager.get_instance().get_logger()
            cls.__utils = XlsxUtils(logger)
        return cls.__utils

    def __init__(self, logger):
        self.__logger = logger
        self.__sheet = None

    def get_sheets_names(self, file_path):
        workbook = xlrd.open_workbook(file_path)
        ret_names = []
        for sheet in workbook.sheets():
            ret_names.append(sheet.name)
        return ret_names

    # --------------------------------------------------------------
    # Read data from excel sheet
    # --------------------------------------------------------------
    def load_sheet_data(self, file_path, sheet_name):
        if not os.path.exists(file_path):
            raise FileNotFoundError('Excel file is not exist: ' + file_path)

        self.__logger.info('load file %s sheet %s' % (file_path, sheet_name))
        workbook = xlrd.open_workbook(file_path)
        self.__sheet = workbook.sheet_by_name(sheet_name)
        return self

    def read_header_row(self):
        self.verify_read_sheet_data()
        ret_header = []
        for cell in self.__sheet.get_rows().__next__():
            ret_header.append(cell.value)

        return ret_header

    def read_all_rows_by_sheet(self, is_include_header=False):
        self.verify_read_sheet_data()
        ret_rows = []
        for row in self.__sheet.get_rows():
            tmp_row = []
            for cell in row:
                tmp_row.append(str(cell.value))
            ret_rows.append(tmp_row)

        return ret_rows[1:] if is_include_header else ret_rows

    def read_values_by_cloumn(self, col_num, is_include_header=False):
        self.verify_read_sheet_data()
        ret_vals = []
        for row in self.__sheet.get_rows():
            ret_vals.append(row[col_num].value)

        return ret_vals[1:] if is_include_header else ret_vals

    def read_cell_value(self, row_num, col_num):
        self.verify_read_sheet_data()
        ret_val = self.__sheet.cell(row_num, col_num).value
        return str(ret_val)

    def verify_read_sheet_data(self):
        if self.__sheet is None:
            raise Exception('Pls load sheet data first!')

    # --------------------------------------------------------------
    # Write data to excel sheet
    # --------------------------------------------------------------
    # TODO:


if __name__ == '__main__':

    log_manager = LogManager.biuld(Constants.LOG_FILE_PATH).get_instance()
    xlsx = XlsxUtils.get_instance()

    sheet_name = 'Module01'
    file_path = os.path.join(os.path.dirname(os.getcwd()), 'apitest', 'TestCases.xlsx')
    print(xlsx.get_sheets_names(file_path))

    xlsx.load_sheet_data(file_path, sheet_name)
    print(xlsx.read_all_rows_by_sheet())
    # excel cell index start with (0,0)
    # print('test cases:', xlsx.read_values_by_cloumn(1))
    # print('1st case name:', xlsx.read_cell_value(1, 1))

    log_manager.clear_log_handles()
    print('xlsx utils test DONE.')
