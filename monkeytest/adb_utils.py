#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''

import os
from constants import Constants
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
    def is_package_on_top(pkg_name):
        cmd = 'adb shell dumpsys activity | findstr mFocusedActivity | findstr ' + pkg_name
        tmp_lines = SysUtils.run_sys_cmd(cmd)
        return len(tmp_lines) != 0

    @classmethod
    def dump_logcat_by_tag(cls, tag, file_path=Constants.TEST_FILE_PATH):
        cmd = 'adb logcat -c && adb logcat -s %s -v time -d > %s' % (tag, file_path)
        return SysUtils.run_sys_cmd(cmd)

    @classmethod
    def dump_app_info(cls, app, file_path=Constants.TEST_FILE_PATH):
        cmd = 'adb shell dumpsys package %s > %s' % (app, file_path)
        return SysUtils.run_sys_cmd(cmd)

    @classmethod
    def dump_android_props(cls, file_path=Constants.TEST_FILE_PATH):
        cmd = 'adb shell getprop > %s' % file_path
        return SysUtils.run_sys_cmd(cmd)

    @classmethod
    def dump_anr_files(cls, save_path):
        cmd = 'adb pull /data/anr %s' % save_path
        return SysUtils.run_sys_cmd(cmd)

    @classmethod
    def clear_anr_dir(cls):
        cmd = 'adb shell rm /data/anr/*'
        return SysUtils.run_sys_cmd(cmd)

    @classmethod
    def dump_tombstone_files(cls, save_path):
        cmd = 'adb pull /data/tombstones %s' % save_path
        return SysUtils.run_sys_cmd(cmd)

    @classmethod
    def clear_tombstone_dir(cls):
        cmd = 'adb shell rm /data/tombstones/*'
        return SysUtils.run_sys_cmd(cmd)

    # --------------------------------------------------------------
    # Process handle function
    # --------------------------------------------------------------
    @classmethod
    def get_process_id_by_name(cls, p_name):
        cmd = 'adb shell ps | findstr %s' % p_name
    
        for line in os.popen(cmd).readlines():
            if p_name in line:
                return line.split()[1]  # process id
        return ''

    @classmethod
    def kill_process_by_pid(cls, p_id):
        cmd = 'adb shell kill %s' % p_id
        return SysUtils.run_sys_cmd(cmd)

    # --------------------------------------------------------------
    # IO function
    # --------------------------------------------------------------
    @classmethod
    def create_dir_on_shell(cls, dir_path):
        cmd = 'adb shell mkdir %s' % (dir_path)
        return os.popen(cmd).readlines()

    @classmethod
    def remove_file_on_shell(cls, file_path):
        cmd = 'adb shell rm -rf %s' % file_path
        return os.popen(cmd).readlines()


if __name__ == '__main__':
    
    AdbUtils.is_adb_devices_connect()
    print('adb manager test DONE!')
