# -*- coding: utf-8 -*-
'''
Created on 2019-01-18
@author: zhengjin

Read json body from excel, and sent post request.
libs: xlrd (excel read), xlwt (excel write)
'''

import json
import os
import xlrd

from urllib import parse, request


CHARSET_UTF8 = 'utf-8'

class api_test_by_excel(object):

    def __init__(self, file_path):
        if len(file_path) == 0:
            raise IOError('input excel file path is null!')
        if not os.path.exists(file_path):
            raise IOError('input excel file path is not exist:', file_path)
        self.workbook = xlrd.open_workbook(file_path)

    def read_req_json_body_from_excel(self, req_col_num):
        sheets = self.workbook.sheet_names()
        for sheet in sheets:
            print('excel sheet:', sheet)

        sheet_api_test = self.workbook.sheet_by_index(1)

        # for i in range(4, sheet_api_test.nrows):
        for i in range(3, 6):
            # get request json body
            req_json_body = sheet_api_test.cell(i, req_col_num).value
            if req_json_body is None or len(req_json_body) == 0:
                print('loop at %d, request body is null and skip' % i)
                continue
            print('loop at %d, request json body: %s' % (i, req_json_body))

            # get expect response json body
            resp_json_body = sheet_api_test.cell(i, resp_col_num).value
            if resp_json_body is None or len(resp_json_body) == 0:
                print('loop at %d, expect response body is null and skip' % i)
                continue
            json_body = json.loads(resp_json_body)
            print('expect resp json: status => %s, score => %s' %
                (json_body['status'], json_body['score']))


def http_post_req(url, req_json_body):
    header_dict = {'Content-Type': 'application/json'}
    req = request.Request(url=url, data=req_json_body, headers=header_dict)
    resp = request.urlopen(req)
    print('resp code:', resp.status)
    print('resp headers:', resp.headers)

    resp_body = resp.read().decode(CHARSET_UTF8)
    print('resp body:\n' + resp_body)


if __name__ == '__main__':

    test_json = {'status': 'OK', 'score': 0.91}
    print('test json body:', json.dumps(test_json))

    is_read_json_body = True
    if is_read_json_body:
        file_path = os.path.join(
            os.getenv('HOME'), 'Downloads/tmp_files/smoke_test.xlsx')
        req_col_num = 5
        resp_col_num = 7
        read_json_body_from_excel(file_path, req_col_num, resp_col_num)

    is_post_req = False
    if is_post_req:
        url = 'http://localhost:17891/index'
        req_json = {'key1': 'value1'}
        req_json_text = json.dumps(req_json).encode(encoding=CHARSET_UTF8)
        http_post_req(url, req_json_text)

    print('excel read and post demo done.')
