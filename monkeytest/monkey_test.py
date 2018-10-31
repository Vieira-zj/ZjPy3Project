# -*- coding: utf-8 -*-
'''
Created on 2018-10-29

@author: zhengjin
'''

import os
import subprocess
import threading
from adb_utils import AdbUtils
from constants import Constants
from monkey_monitor import MonkeyMonitor
from log_manager import LogManager
from sys_utils import SysUtils


class MonkeyTest(object):
    '''
    classdocs
    '''

    # --------------------------------------------------------------
    # Init
    # --------------------------------------------------------------
    def __init__(self, test_pkg_name, run_mins=Constants.RUN_MINS):
        '''
        Constructor
        '''
        self.test_pkg_name = test_pkg_name

        cur_time = SysUtils.get_current_date_and_time()
        self.log_root_path = os.path.join(os.getcwd(), 'MonkeyReports')
        self.log_dir_path_for_win = os.path.join(self.log_root_path, cur_time)
        self.log_dir_path_for_shell = '/data/local/tmp/monkey_test_logs'

        self.exec_log_path = os.path.join(self.log_dir_path_for_win, 'run_log.log')
        self.monkey_log_path = os.path.join(self.log_dir_path_for_win, 'monkey_log.log')
        self.device_props_file_path = os.path.join(self.log_dir_path_for_win, 'device_props.log')
        self.app_dump_file_path = os.path.join(self.log_dir_path_for_win, 'app_info.log')
        self.logcat_log_path_for_shell = '%s/%s' % (self.log_dir_path_for_shell, 'logcat_log.log')

        SysUtils.create_dir_on_win(self.log_dir_path_for_win)
        self.log_manager = LogManager(self.exec_log_path)
        self.logger = self.log_manager.get_logger()
        self.sysutils = SysUtils(self.logger)
        self.adbutils = AdbUtils(self.logger)
        self.monitor = MonkeyMonitor(self.logger, run_mins)
        
    # --------------------------------------------------------------
    # Processes
    # --------------------------------------------------------------
    def __build_monkey_cmd(self):
        monkey_cmd = 'adb shell monkey --throttle 500 -p %s' % self.test_pkg_name

        monkey_launch_params = '-c android.intent.category.MONKEY -c android.intent.category.LAUNCHER -c ' + \
            'android.intent.category.DEFAULT --monitor-native-crashes --kill-process-after-error'
        monkey_ignore = ''
        if Constants.IS_MONKEY_CRASH_IGNORE:
            monkey_ignore = '--ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes'
        monkey_actions_pct = '--pct-touch 65 --pct-motion 20 --pct-trackball 5 --pct-nav 0 ' + \
            '--pct-majornav 5 --pct-syskeys 5 --pct-appswitch 0 --pct-flip 0 --pct-anyevent 0'
        monkey_format = '-v -v -v %s > %s' % (Constants.MONKEY_TOTAL_RUN_TIMES, self.monkey_log_path)

        return ' '.join((monkey_cmd, monkey_launch_params, monkey_ignore, monkey_actions_pct, monkey_format))

    def __run_monkey_subprocess(self):
        return subprocess.Popen(self.__build_monkey_cmd(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def __run_logcat_subprocess(self):
        cmd = 'adb logcat -c && adb logcat -f %s -v threadtime *:%s' % (self.logcat_log_path_for_shell, Constants.LOGCAT_LOG_LEVEL) 
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # --------------------------------------------------------------
    # Adb and shell utils
    # --------------------------------------------------------------
    def __is_device_busy(self, lines):
        for line in lines:
            if 'busy' in line:
                self.logger.error(line)
                self.logger.error('Error, monkey test exit because of device busy!')
                exit(1)
    
    def __create_log_dir_for_shell(self, dir_path):
        self.__is_device_busy(AdbUtils.create_dir_on_shell(dir_path))
        
    def __clear_log_dir_for_shell(self):
        self.__is_device_busy(AdbUtils.remove_files_on_shell(self.log_dir_path_for_shell))

    def __pull_all_testing_logs(self):
        cmd_pull_logcat_log = 'adb pull %s %s' % (self.logcat_log_path_for_shell, self.log_dir_path_for_win)
        self.sysutils.run_sys_cmd(cmd_pull_logcat_log)

        self.__pull_latest_anr_files()
        self.adbutils.dump_tombstone_files(self.log_dir_path_for_win)
    
    def __pull_latest_anr_files(self):
        '''
        Get anr files in 24 hours.
        '''
        cmd = 'adb shell "find /data/anr/ -name \'*.txt\' -mtime -1 2>/dev/null"'
        anr_files = self.sysutils.run_sys_cmd_and_ret_lines(cmd)
        
        save_path = r'%s\anr' % self.log_dir_path_for_win
        self.sysutils.create_dir_on_win(save_path)
        for f in anr_files:
            f = f.strip('\r\n')
            if len(f) == 0:
                continue
            cmd = 'adb pull %s %s' % (f, save_path)
            self.sysutils.run_sys_cmd(cmd)
    
    # --------------------------------------------------------------
    # Monkey Test Main
    # --------------------------------------------------------------
    def __test_setup_main(self):
        if not self.adbutils.is_devices_connected():
            self.logger.error('No devices connected!')
            exit(1)

        # shell env setup
        self.adbutils.clear_anr_dir()
        self.adbutils.clear_tombstone_dir()
        self.__clear_log_dir_for_shell()
        self.__create_log_dir_for_shell(self.log_dir_path_for_shell)
    
        # win env setup
        self.adbutils.dump_device_props(self.device_props_file_path)
        self.adbutils.dump_app_info(Constants.PKG_NAME_ZGB, self.app_dump_file_path)

    def __test_main(self):
        self.logger.info('Start logcat process.')
        logcat_p = self.__run_logcat_subprocess()
        self.logger.info('Start monkey main process.')
        monkey_p = self.__run_monkey_subprocess()
    
        self.logger.info('Start monkey monitor process.')
        monitor_t = threading.Thread(target=self.monitor.process_monkey_monitor_main)
        monitor_t.start()
        monitor_t.join()

        monkey_p.kill()
        logcat_p.kill()

    def __test_clearup_main(self):
        # the adb connection maybe disconnect when running the monkey
        if self.adbutils.is_devices_connected():
            self.__pull_all_testing_logs()
            self.adbutils.clear_app_data(self.test_pkg_name)
        else:
            self.logger.error('Device disconnect.')
        self.log_manager.clear_log_handles()
    
    def mokeytest_main(self):
        self.__test_setup_main()
        self.__test_main()
        self.__test_clearup_main()
    
    
if __name__ == '__main__':
    
    test = MonkeyTest(Constants.PKG_NAME_ZGB, 60)
    test.mokeytest_main()
    print('Monkey test DONE.')
