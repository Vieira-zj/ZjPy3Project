# -*- coding: utf-8 -*-
'''
Created on 2019-03-06
@author: zhengjin
'''

import os
import sys
import configparser

sys.path.append(os.getenv('PYPATH'))
from utils import Constants


class LoadConfigs(object):

    SECTION_TEST_ENV = 'testenv'
    SECTION_MOCK = 'mockserver'
    SECTION_EMAIL = 'emails'

    configs = {}

    @classmethod
    def load_configs(cls, cfg_file_path):
        if len(cfg_file_path) == 0:
            raise ValueError('config file path is null!')
        if not os.path.exists(cfg_file_path):
            raise FileNotFoundError('configs file %s is not found!' % cfg_file_path)

        cfg_reader = configparser.ConfigParser()
        cfg_reader.read(cfg_file_path)

        for section in cfg_reader.sections():
            options = cfg_reader.options(section)
            tmp_dict = {}
            for option in options:
                tmp_dict[option] = cfg_reader.get(section, option)
            cls.configs[section] = tmp_dict

    @classmethod
    def get_testenv_configs(cls):
        cls.__verify_configs()
        return cls.configs.get(cls.SECTION_TEST_ENV)

    @classmethod
    def get_mock_configs(cls):
        cls.__verify_configs()
        return cls.configs.get(cls.SECTION_MOCK)

    @classmethod
    def get_email_configs(cls):
        cls.__verify_configs()
        return cls.configs.get(cls.SECTION_EMAIL)

    @classmethod
    def __verify_configs(cls):
        if len(cls.configs) == 0:
            raise Exception('Pls load configs first!')


if __name__ == '__main__':

    cfg_file_path = os.path.join(os.path.dirname(os.getcwd()), 'configs.ini')
    LoadConfigs.load_configs(cfg_file_path)
    print('test http server url: %s:%s'
          % (LoadConfigs.get_mock_configs().get('ip'), LoadConfigs.get_mock_configs().get('port')))

    email_configs = LoadConfigs.get_email_configs()
    print('mail user pwd:', email_configs.get('mail_pwd'))
    print('mail content:', email_configs.get('content'))

    print('read ini configs DONE.')
