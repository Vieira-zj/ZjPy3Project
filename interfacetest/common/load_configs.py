# -*- coding: utf-8 -*-
'''
Created on 2019-03-06

@author: zhengjin
'''

import os
import sys
import configparser

sys.path.append('../../')
from utils import Constants
from utils import LogManager 
from utils import SysUtils


class LoadConfigs(object):

    __GROUP_HTTP_SERVER_TEST = 'http-svc-test'

    def __init__(self, cfg_file_path=''):
        if len(cfg_file_path) == 0:
            cfg_file_path = os.path.join(os.path.dirname(os.getcwd()), 'configs.ini')

        log_file = 'test_log_%s' % SysUtils.get_current_date()
        self.__log_file_path = os.path.join(os.path.dirname(os.getcwd()), 'outputs', 'logs', log_file)
        self.__log_manager = LogManager(self.__log_file_path)
        self.__logger = self.__log_manager.get_logger()

        self.__cfg_reader = configparser.ConfigParser()
        self.__load_configs(cfg_file_path)

    def __load_configs(self, cfg_file_path):
        if not os.path.exists(cfg_file_path):
            raise FileNotFoundError('configs file %s is not exist!' % cfg_file_path)

        self.__logger.info('load configs in file:', cfg_file_path)
        self.__cfg_reader.read(cfg_file_path)

    def get_svc_test_ip(self):
        return self.__cfg_reader.get(self.__GROUP_HTTP_SERVER_TEST, 'ip')

    def get_svc_test_port(self):
        return self.__cfg_reader.get(self.__GROUP_HTTP_SERVER_TEST, 'port')


if __name__ == '__main__':

    cfg = LoadConfigs()
    print('test http server url: %s:%s' % (cfg.get_svc_test_ip(), cfg.get_svc_test_port()))

    print('read ini configs DONE.')
