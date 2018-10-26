#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''

from log_manager import LogManager
from sys_utils import SysUtils


class AdbUtils(object):

    logger = LogManager.getLoggerInstance()
    
    def __init__(self):
        pass

    @classmethod
    def is_adb_devices_connect(cls):
        cls.logger.debug('check adb devices connected.')
        
#         cmd = 'adb devices -l'
        cmd = 'adb get-serialno'
        ret_content = SysUtils.run_sys_cmd_and_ret_content(cmd)
        if len(ret_content) == 0:
            return False
        if ('unknown' in ret_content) or ('error' in ret_content):
            return False
        cls.logger.info('connected devices: \n%s', ret_content)
        return True

    @classmethod
    def dump_logcat_by_tag(cls):
#       TODO:
        pass
    

if __name__ == '__main__':
    
    AdbUtils.is_adb_devices_connect()
    print('adb manager test DONE!')
