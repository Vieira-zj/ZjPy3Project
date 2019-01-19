# -*- coding: utf-8 -*-
'''
Created on 2019-01-18
@author: zhengjin

Read json body from excel, and sent post request.
'''

import json
import xlrd

from urllib import parse, request


CHARSET_UTF8 = 'utf-8'


def read_req_json_body_from_excel(file_path, col_num):
    if len(file_path) == 0:
        raise Exception('excel file path is null!')

    workbook = xlrd.open_workbook(file_path)

    sheets = workbook.sheet_names()
    for sheet in sheets:
        print('excel sheet:', sheet)

    sheet_api_test = workbook.sheet_by_index(1)
    # for i in range(4, sheet_api_test.nrows):
    for i in range(4, 10):
        print('request json body:', sheet_api_test.cell(i, col_num).value)


def http_post_req(url, req_json_body):
    header_dict = {'Content-Type': 'application/json'}
    req = request.Request(url=url, data=req_json_body, headers=header_dict)
    resp = request.urlopen(req)
    print('resp code:', resp.status)
    print('resp headers:', resp.headers)

    resp_body = resp.read().decode(CHARSET_UTF8)
    print('resp body:\n' + resp_body)


if __name__ == '__main__':

    # file_path = '/Users/zhengjin/Downloads/tmp_files/smoke_test.xlsx'
    # col_num = 5
    # read_req_json_body_from_excel(file_path, col_num)

    url = 'http://localhost:17891/index'
    req_json = {'key1': 'value1'}
    req_json_text = json.dumps(req_json).encode(encoding=CHARSET_UTF8)
    http_post_req(url, req_json_text)

    print('excel read and post demo done.')
