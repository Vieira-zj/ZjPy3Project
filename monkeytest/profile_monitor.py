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
    __log_root_dir_path = '/sdcard/AndroidPropertyTool4'
    __hand_log_dir = 'handTest'
    __hand_log_dir_path = __log_root_dir_path + '/' + __hand_log_dir

    def __init__(self, logger):
        '''
        Constructor
        '''
        self.__logger = logger
        self.__sys_utils = SysUtils(logger)
        self.__adb_utils = AdbUtils(logger)

    # --------------------------------------------------------------
    # Start Monitor
    # --------------------------------------------------------------
    def clear_itest_logs(self):
        cmd = 'adb shell "cd %s;rm -rf %s*"' % (self.__log_root_dir_path, self.__hand_log_dir)
        self.__sys_utils.run_sys_cmd(cmd)
        if not self.__sys_utils.run_sys_cmd(cmd):
            raise Exception('clear iTest log files failed!')

    def __launch_itest(self):
        cmd = 'adb shell am start ' + self.__itest_pkg_name + '/' + self.__itest_boot_act
        self.__sys_utils.run_sys_cmd(cmd)
        
        for i in range(0, 3):
            if self.__adb_utils.is_package_on_top(self.__itest_pkg_name):
                return
            time.sleep(1)
        raise Exception('launch iTest app failed!')

    def __is_itest_logfile_created(self):
        cmd = 'adb shell "cd %s;ls|grep %s"' % (self.__log_root_dir_path, self.__hand_log_dir)
        return len(self.__sys_utils.run_sys_cmd_and_ret_content(cmd)) != 0

    def __click_itest_monitor_btn(self):
        cmd = 'adb shell input tap 800 1880'
        return self.__sys_utils.run_sys_cmd(cmd)
    
    def start_monitor(self):
        self.clear_itest_logs()
        self.__launch_itest()
        time.sleep(1)
        self.__click_itest_monitor_btn()
        time.sleep(1)
        if not self.__is_itest_logfile_created():
            raise Exception('start iTest monitor failed!')
    
    # --------------------------------------------------------------
    # Running Monitor
    # --------------------------------------------------------------
    def __is_itest_process_running(self):
        cmd = 'adb shell "ps | grep %s"' % self.__itest_pkg_name
        if len(self.__sys_utils.run_sys_cmd_and_ret_content(cmd)) == 0:
            return False
        return True
    
    def __get_cpu_logfile_record_time(self):
        file_name = 'cpuSystem.txt'
        cmd = 'adb shell "cd %s;tail -n 1 %s"' % (self.__hand_log_dir_path, file_name)
        last_line = self.__sys_utils.run_sys_cmd_and_ret_content(cmd)
        return last_line.split()[0]  # record time
    
    def __is_cpu_logfile_updated(self):
        before_record_time = self.__get_cpu_logfile_record_time()
        self.__logger.info('before time: ' + before_record_time)
        time.sleep(2)
        after_record_time = self.__get_cpu_logfile_record_time()
        self.__logger.info('after time: ' + after_record_time)
        return before_record_time != after_record_time
    
    def __is_itest_running(self):
        if self.__is_itest_process_running() and self.__is_cpu_logfile_updated():
            return True
        return False

    def running_monitor(self, run_mins, interval=5):
        run_secs = run_mins * 60
        start = time.perf_counter()
        while 1:
            time.sleep(interval)
            if not self.__is_itest_running():
                self.__logger.error('iTest process is NOT running!')
                return
            if time.perf_counter() - start >= run_secs and self.__is_itest_running():
                self.stop_monitor()
                return

    # --------------------------------------------------------------
    # Stop Monitor
    # --------------------------------------------------------------
    def __force_stop_itest(self):
        cmd = 'adb shell am force-stop ' + self.__itest_pkg_name
        self.__sys_utils.run_sys_cmd(cmd)

    def stop_monitor(self):
        self.__launch_itest()
        time.sleep(1)
        self.__click_itest_monitor_btn()
        time.sleep(1)
        self.__force_stop_itest()

    def __clear_local_itest_logs(self, dir_path):
        SysUtils.delete_files_in_dir(dir_path)
    
    def pull_itest_logfiles(self, local_save_path):
        if len(local_save_path) == 0:
            self.__logger.warn('skip dump iTest logs!')
            return
        
        self.__clear_local_itest_logs(os.path.join(local_save_path, self.__hand_log_dir))
        cmd = 'adb pull %s %s' % (self.__hand_log_dir_path, local_save_path)
        if not self.__sys_utils.run_sys_cmd(cmd):
            self.__logger.error('dump iTest logs failed!')


if __name__ == '__main__':

    from monkeytest.constants import Constants
    from monkeytest.log_manager import LogManager

    manager = LogManager(Constants.LOG_FILE_PATH)
    logger = manager.get_logger()
    
    monitor = ProfileMonitor(logger)
    monitor.start_monitor()
    monitor.running_monitor(0.5)
    time.sleep(1)
    monitor.pull_itest_logfiles(r'D:\JDTestLogs')
    
    manager.clear_log_handles()
    
    print('profile monitor test DONE.')
