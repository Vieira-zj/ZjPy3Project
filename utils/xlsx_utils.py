# -*- coding: utf-8 -*-
'''
Created on 2019-01-18

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
    def get_instance(cls, logger, file_path, sheet_name):
        if cls.__utils is None:
            cls.__utils = XlsxUtils(logger, file_path, sheet_name)
        return cls.__utils

    def __init__(self, logger, file_path, sheet_name):
        if not os.path.exists(file_path):
            raise FileNotFoundError('Excel file is not exist: ' + file_path)

        self.__logger = logger
        self.__sheet = None
        self.load_sheet_data(file_path, sheet_name)

    def load_sheet_data(self, file_path, sheet_name):
        self.__logger.info('load file %s sheet %s' % (file_path, sheet_name))
        workbook = xlrd.open_workbook(file_path)
        self.__sheet = workbook.sheet_by_name(sheet_name)

    def read_cel_value(self, row_num, col_num):
        return self.__sheet.cell(row_num, col_num)


if __name__ == '__main__':

    file_path = os.path.join(os.path.dirname(os.getcwd()), 'interfacetest', 'TestCases.xlsx')
    sheet_name = 'Module01'

    log_manager = LogManager(Constants.LOG_FILE_PATH)
    xlsx = XlsxUtils.get_instance(log_manager.get_logger(), file_path, sheet_name)
    print(xlsx.read_cel_value(1, 1))

    log_manager.clear_log_handles()

    print('xlsx utils test DONE.')
