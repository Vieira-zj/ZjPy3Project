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


class LoadConfigs(object):

    SECTION_TEST = 'test'
    SECTION_PROPHET = 'prophet'

    # save all configs
    test_configs = {}

    def __init__(self, logger, cfg_file_path=''):
        if len(cfg_file_path) == 0:
            cfg_file_path = os.path.join(os.path.dirname(os.getcwd()), 'configs.ini')
        if not os.path.exists(cfg_file_path):
            raise FileNotFoundError('configs file %s is not exist!' % cfg_file_path)

        self.__logger = logger
        self.__load_configs(cfg_file_path)

    def __load_configs(self, cfg_file_path):
        self.__logger.info('load configs from: ' + cfg_file_path)
        self.__cfg_reader = configparser.ConfigParser()
        self.__cfg_reader.read(cfg_file_path)

        for section in self.__cfg_reader.sections():
            options = self.__cfg_reader.options(section)
            tmp_dict = {}
            for option in options:
                tmp_dict[option] = self.__cfg_reader.get(section, option)
            self.test_configs[section] = tmp_dict

    def get_svc_test_ip(self):
        return self.test_configs.get(self.SECTION_TEST).get('ip')

    def get_svc_test_port(self):
        return self.test_configs.get(self.SECTION_TEST).get('port')


if __name__ == '__main__':

    log_manager = LogManager(Constants.LOG_FILE_PATH)
    cfg = LoadConfigs(log_manager.get_logger())
    print('test http server url: %s:%s' % (cfg.get_svc_test_ip(), cfg.get_svc_test_port()))
    print('prophet user id:', cfg.test_configs.get(LoadConfigs.SECTION_PROPHET).get('id'))

    log_manager.clear_log_handles()
    print('read ini configs DONE.')
