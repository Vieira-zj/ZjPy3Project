#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''

import re
import os
from monkeytest.sys_utils import SysUtils


class AdbUtils(object):

    def __init__(self, logger):
        self.logger = logger
        self.sys_utils = SysUtils(self.logger)

    @classmethod
    def print_adb_info(cls):
        cmd = 'adb version'
        return os.popen(cmd).read()

    def is_devices_connected(self):
        # support one device
        self.logger.debug('check adb devices connected.')
        
        cmd = 'adb devices -l'
#         cmd = 'adb get-serialno'
        ret_content = self.sys_utils.run_sys_cmd_and_ret_content(cmd)
        if len(ret_content.strip()) == 0:
            return False
        if re.search('unknown|error|offline', ret_content):
            return False
        self.logger.info('connected devices: \n%s', ret_content)
        return True

    def is_package_on_top(self, pkg_name):
        cmd = 'adb shell dumpsys activity | findstr mFocusedActivity | findstr ' + pkg_name
        tmp_lines = self.sys_utils.run_sys_cmd(cmd)
        return len(tmp_lines) != 0

    def dump_logcat_by_tag(self, tag, file_path):
        cmd = 'adb logcat -c && adb logcat -s %s -v time -d > %s' % (tag, file_path)
        return self.sys_utils.run_sys_cmd(cmd)

    def dump_app_info(self, app_name, file_path):
        if os.path.exists(file_path):
            self.logger.warning('file %s is exist and will be override!' % file_path)
        cmd = 'adb shell dumpsys package %s > %s' % (app_name, file_path)
        return self.sys_utils.run_sys_cmd(cmd)

    def clear_app_data(self, pkg_name):
        cmd = 'adb shell pm clear %s' % pkg_name
        return self.sys_utils.run_sys_cmd(cmd)

    def dump_device_props(self, file_path):
        if os.path.exists(file_path):
            self.logger.warning('file %s is exist and will be override!' % file_path)
        cmd = 'adb shell getprop > %s' % file_path
        return self.sys_utils.run_sys_cmd(cmd)

    def dump_anr_files(self, save_path):
        cmd = 'adb pull /data/anr %s' % save_path
        return self.sys_utils.run_sys_cmd(cmd)

    def clear_anr_dir(self):
        cmd = 'adb shell "rm -f /data/anr/* 2>/dev/null"'
        return self.sys_utils.run_sys_cmd(cmd)

    def dump_tombstone_files(self, save_path):
        cmd = 'adb pull /data/tombstones %s' % save_path
        return self.sys_utils.run_sys_cmd(cmd)

    def clear_tombstone_dir(self):
        cmd = 'adb shell "rm -f /data/tombstones/* 2>/dev/null"'
        return self.sys_utils.run_sys_cmd(cmd)

    # --------------------------------------------------------------
    # Process handle function
    # --------------------------------------------------------------
    def get_process_id_by_name(self, p_name):
        cmd = 'adb shell ps | findstr %s' % p_name
        for line in os.popen(cmd).readlines():
            if p_name in line:
                return line.split()[1]  # process id
        return ''

    def kill_process_by_pid(self, p_id):
        if p_id is None or len(p_id) == 0:
            return
        cmd = 'adb shell kill %s' % p_id
        return self.sys_utils.run_sys_cmd(cmd)

    # --------------------------------------------------------------
    # IO function
    # --------------------------------------------------------------
    def create_dir_on_shell(self, dir_path):
        cmd = 'adb shell "mkdir %s 2>/dev/null"' % dir_path
        return self.sys_utils.run_sys_cmd_and_ret_lines(cmd)

    def remove_files_on_shell(self, file_path):
        cmd = 'adb shell "rm -rf %s 2>/dev/null"' % file_path
        return self.sys_utils.run_sys_cmd_and_ret_lines(cmd)


if __name__ == '__main__':
    
    from constants import Constants
    from log_manager import LogManager

    manager = LogManager(Constants.LOG_FILE_PATH)
    logger = manager.get_logger()
    utils = AdbUtils(logger)
    print(utils.is_devices_connected())
    print('Monkey pid:', utils.get_process_id_by_name('monkey'))
    manager.clear_log_handles()
    
    print('adb manager test DONE.')
