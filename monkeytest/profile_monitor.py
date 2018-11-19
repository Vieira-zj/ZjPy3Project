# -*- coding: utf-8 -*-
'''
Created on 2018-11-19

@author: zhengjin
'''

import time
import os
from monkeytest.adb_utils import AdbUtils
from monkeytest.sys_utils import SysUtils


class ProfileMonitor(object):
    '''
    Android app profile monitor by iTest.
    '''

    __itest_pkg_name = 'iflytek.testTech.propertytool'
    __itest_boot_act = 'iflytek.testTech.propertytool.activity.BootActivity' 
    __log_root_dir = '/sdcard/AndroidPropertyTool4'
    __hand_log_dir = __log_root_dir + '/handTest'

    def __init__(self, logger, local_log_dir):
        '''
        Constructor
        '''
        self.logger = logger
        self.sys_utils = SysUtils(logger)
        self.adb_utils = AdbUtils(logger)
        self.local_log_dir = local_log_dir

    # --------------------------------------------------------------
    # Start Monitor
    # --------------------------------------------------------------
    def clear_itest_logs(self):
        cmd = 'adb shell "cd %s;rm -rf handTest*"' % self.__log_root_dir
        self.sys_utils.run_sys_cmd(cmd)
        if not self.sys_utils.run_sys_cmd(cmd):
            raise Exception('clear iTest log files failed!')

    def __launch_itest(self):
        cmd = 'adb shell am start ' + self.__itest_pkg_name + '/' + self.__itest_boot_act
        self.sys_utils.run_sys_cmd(cmd)
        
        for i in range(0, 3):
            if self.adb_utils.is_package_on_top(self.__itest_pkg_name):
                return
            time.sleep(1)
        raise Exception('launch iTest app failed!')

    def __is_itest_logfile_created(self):
        cmd = 'adb shell "cd %s;ls|grep handTest"' % self.__log_root_dir
        return len(self.sys_utils.run_sys_cmd_and_ret_content(cmd)) != 0

    def __click_itest_monitor_btn(self):
        cmd = 'adb shell input tap 800 1880'
        return self.sys_utils.run_sys_cmd(cmd)
    
    def start_monitor(self):
        self.clear_itest_logs()
        self.__launch_itest()
        time.sleep(1)
        self.__click_itest_monitor_btn()
        time.sleep(1)
        if not self.__is_itest_logfile_created():
            raise Exception('start iTest monitor failed!')
    
    # --------------------------------------------------------------
    # Monitor Running
    # --------------------------------------------------------------
    def __is_itest_process_running(self):
        cmd = 'adb shell "ps | grep %s"' % self.__itest_pkg_name
        if len(self.sys_utils.run_sys_cmd_and_ret_content(cmd)) == 0:
            return False
        return True
    
    def __get_cpu_logfile_record_time(self):
        file_name = 'cpuSystem.txt'
        cmd = 'adb shell "cd %s;tail -n 1 %s"' % (self.__hand_log_dir, file_name)
        last_line = self.sys_utils.run_sys_cmd_and_ret_content(cmd)
        return last_line.split()[0]  # record time
    
    def __is_cpu_logfile_updated(self):
        before_record_time = self.__get_cpu_logfile_record_time()
        self.logger.info('before time: ' + before_record_time)
        time.sleep(2)
        after_record_time = self.__get_cpu_logfile_record_time()
        self.logger.info('after time: ' + after_record_time)
        return before_record_time != after_record_time
    
    def is_itest_running(self):
        if self.__is_itest_process_running() and self.__is_cpu_logfile_updated():
            return True
        return False

    # --------------------------------------------------------------
    # Stop Running
    # --------------------------------------------------------------
    def __force_stop_itest(self):
        cmd = 'adb shell am force-stop ' + self.__itest_pkg_name
        self.sys_utils.run_sys_cmd(cmd)

    def __pull_itest_logfiles(self, local_save_path):
        cmd = 'adb pull %s %s' % (self.__hand_log_dir, local_save_path)
        if not self.sys_utils.run_sys_cmd(cmd):
            self.logger.error('dump iTest logs failed!')

    def stop_monitor(self):
        self.__launch_itest()
        self.__click_itest_monitor_btn()
        time.sleep(1)
        self.__force_stop_itest()
        time.sleep(1)
        self.__pull_itest_logfiles(self.local_log_dir)


if __name__ == '__main__':

    from monkeytest.constants import Constants
    from monkeytest.log_manager import LogManager

    manager = LogManager(Constants.LOG_FILE_PATH)
    logger = manager.get_logger()
    monitor = ProfileMonitor(logger, 'D:\JDTestLogs')
    monitor.start_monitor()
    time.sleep(10)
    if not monitor.is_itest_running():
        exit(1)
    time.sleep(5)
    monitor.stop_monitor()
    
    print('profile monitor test DONE.')
