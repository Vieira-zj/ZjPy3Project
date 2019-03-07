# -*- coding: utf-8 -*-
'''
Created on 2019-03-06

@author: zhengjin
'''

import os
import sys
import json
import requests

sys.path.append('../')
from utils import LogManager
from utils import Constants


class HttpUtils(object):

    __utils = None

    @classmethod
    def get_instance(cls, logger):
        if cls.__utils is None:
            cls.__utils = HttpUtils(logger)
        return cls.__utils

    def __init__(self, logger):
        self.__logger = logger
        self.__headers = {}

    def set_default_headers(self, headers):
        self.__headers = headers
        self.__headers['X-Test'] = 'X-Test-Default'
        return self

    # --------------------------------------------------------------
    # Http Get Request
    # --------------------------------------------------------------
    def send_get_request(self, url, query, headers={}, timeout=1):
        if len(headers) > 0:
            self.__append_headers(headers)

        data_dict = {}
        for entry in query.split('&'):
            k, v = entry.split('=')
            data_dict[k] = v

        resp = None
        try:
            self.__log_request_info(url, query, self.__headers)
            resp = requests.get(url, params=data_dict, headers=self.__headers, timeout=timeout)
            self.__log_response_info(resp)
        except TimeoutError:
            self.__logger.error('http get request time out(%ds)!' % timeout)

        return resp

    # --------------------------------------------------------------
    # Http Post Request
    # --------------------------------------------------------------
    def set_post_request_data(self, url, data, headers={}, timeout=0.5):
        if len(headers) > 0:
            self.__append_headers(headers)

        resp = None
        try:
            self.__log_request_info(url, data, self.__headers)
            resp = requests.post(url, headers=self.__headers, data=data, timeout=timeout)
            self.__log_response_info(resp)
        except TimeoutError:
            self.__logger.error('http post request time out(%ds)!' % timeout)

        return resp

    def set_post_request_json(self, url, json_obj, headers={}, timeout=0.5):
        if len(headers) > 0:
            self.__append_headers(headers)

        resp = None
        try:
            self.__log_request_info(url, json.dumps(json_obj), self.__headers)
            resp = requests.post(url, headers=self.__headers, json=json_obj, timeout=timeout)
            self.__log_response_info(resp)
        except TimeoutError:
            self.__logger.error('http post request time out(%ds)!' % timeout)

        return resp

    def __append_headers(self, headers):
        for key in headers.keys():
            self.__headers[key] = headers[key]

    # --------------------------------------------------------------
    # Print Logs
    # --------------------------------------------------------------
    def __log_request_info(self, url, data, headers={}):
        print('\n\n')
        self.__print_div_line()
        self.__print_with_prefix('Get Request: ' + url)

        self.__print_div_line()
        self.__print_with_prefix('Headers:')
        for item in ['%s: %s' % (k, v) for k, v in headers.items()]:
            self.__print_with_prefix(item)

        self.__print_div_line()
        if data.startswith('{'):
            self.__print_with_prefix('Body: \n' + data[:512])
        else:
            self.__print_with_prefix('Query: ' + data)

        self.__print_div_line()
        self.__print_with_prefix('END')

    def __log_response_info(self, resp):
        self.__print_div_line()
        self.__print_with_prefix('Url: ' + resp.url)
        self.__print_with_prefix('Status Code: %d' % resp.status_code)

        self.__print_div_line()
        self.__print_with_prefix('Headers:')
        for item in ['%s: %s' % (k, v) for k, v in resp.headers.items()]:
            self.__print_with_prefix(item)

        self.__print_div_line()
        self.__print_with_prefix('Body: \n' + str(resp.content))

        self.__print_div_line()
        self.__print_with_prefix('END')

    def __print_div_line(self):
        self.__print_with_prefix('-'*60)

    def __print_with_prefix(self, text):
        print('* ' + text)


if __name__ == '__main__':

    mock_url = 'http://127.0.0.1:17891/index'
    headers = {'X-Test-Method': 'X-Test-Get'}

    log_manager = LogManager(Constants.LOG_FILE_PATH)
    http_utils = HttpUtils.get_instance(log_manager.get_logger()).set_default_headers(headers)

    # get request
    query = 'k1=v1&k2=v2'
    resp = http_utils.send_get_request(mock_url, query)
    assert(resp is not None and resp.status_code == 200)

    # post request
    headers = {'X-Test-Method':'X-Test-Post'}
    data_dict = {'email': '123456@163.com', 'password': '123456'}
    resp = http_utils.set_post_request_data(mock_url, json.dumps(data_dict))
    resp = http_utils.set_post_request_json(mock_url, data_dict)
    assert(resp is not None and resp.status_code == 200)

    log_manager.clear_log_handles()

    print('http utils test DONE.')
