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
    SECTION_EMAIL = 'emails'

    all_configs = {}
    __logger = None

    @classmethod
    def load_configs(cls, cfg_file_path):
        if len(cfg_file_path) == 0:
            raise ValueError('config file path is null!')
        if not os.path.exists(cfg_file_path):
            raise FileNotFoundError('configs file %s is not found!' % cfg_file_path)

        if cls.__logger is None:
            cls.__logger = LogManager.get_instance().get_logger()

        cls.__logger.info('load configs: ' + cfg_file_path)
        cfg_reader = configparser.ConfigParser()
        cfg_reader.read(cfg_file_path)

        for section in cfg_reader.sections():
            options = cfg_reader.options(section)
            tmp_dict = {}
            for option in options:
                tmp_dict[option] = cfg_reader.get(section, option)
            cls.all_configs[section] = tmp_dict

    @classmethod
    def get_svc_test_ip(cls):
        return cls.all_configs.get(cls.SECTION_TEST).get('ip')

    @classmethod
    def get_svc_test_port(cls):
        return cls.all_configs.get(cls.SECTION_TEST).get('port')


if __name__ == '__main__':

    log_manager = LogManager.get_instance(Constants.LOG_FILE_PATH)

    cfg_file_path = os.path.join(os.path.dirname(os.getcwd()), 'configs.ini')
    LoadConfigs.load_configs(cfg_file_path)
    print('test http server url: %s:%s'
          % (LoadConfigs.get_svc_test_ip(), LoadConfigs.get_svc_test_port()))

    mail_configs = LoadConfigs.all_configs.get(LoadConfigs.SECTION_EMAIL)
    print('mail user pwd:', mail_configs.get('mail_pwd'))
    print('mail content:', mail_configs.get('content'))

    log_manager.clear_log_handles()
    print('read ini configs DONE.')
