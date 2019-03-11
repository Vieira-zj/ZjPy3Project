# -*- coding: utf-8 -*-
'''
Created on 2019-03-11

@author: zhengjin
'''

import os
import sys
import pytest

sys.path.append(os.getenv('PYPATH'))
from utils import Constants
from utils import LogManager
from utils import SysUtils
from apitest.common import LoadConfigs
from apitest.common import LoadCases


project_path = os.path.join(os.getenv('PYPATH'), 'apitest')


def load_configs():
    cfg_file_path = os.path.join(project_path, 'configs.ini')
    LoadConfigs.load_configs(cfg_file_path)


def init_logger():
    logdir_path = LoadConfigs.get_testenv_configs().get('logdir_path')
    logdir_path = logdir_path.replace('{project}', project_path)
    logfile_path = os.path.join(
        logdir_path, 'pytest_log_%s.txt' % SysUtils.get_current_date_and_time())
    LogManager.build_logger(logfile_path)


def load_testcases():
    tc_file_path = LoadConfigs.get_testenv_configs().get('tc_file_path')
    tc_file_path = tc_file_path.replace('{project}', project_path)
    LoadCases.get_instance().load_all_cases(tc_file_path)


@pytest.fixture(scope='session')
def setup_test_session(request):
    '''
    session setup: init logger, load configs and testcases.
    '''
    load_configs()
    init_logger()
    load_testcases()

    logger = LogManager.get_logger()
    logger.info('[session setup]: init logger, load configs and testcases done.')

    def clear():
        logger.info('[session clearup] done.')
        LogManager.clear_log_handles()
    request.addfinalizer(clear)


if __name__ == '__main__':

    load_configs()
    init_logger()
    load_testcases()

    tcs = LoadCases.get_instance().get_loaded_tcs()
    LogManager.get_logger().info(tcs)
    LogManager.get_logger().info('conftest DONE.')
    LogManager.clear_log_handles()
