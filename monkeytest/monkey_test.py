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
    def __init__(self, test_pkg_name, run_num, run_mins):
        '''
        Constructor
        '''
        self.test_pkg_name = test_pkg_name
        self.run_num = run_num
        self.run_mins = run_mins

        cur_date = SysUtils.get_current_date()
        self.log_root_path = os.path.join(os.getcwd(), 'MonkeyReports')
        self.log_dir_path_for_win = r'%s\%s_%s' % (self.log_root_path, cur_date, self.run_num)
        self.log_dir_path_for_shell = '/data/local/tmp/monkey_test_logs'

        self.exec_log_path = r'%s\exec_log.log' % self.log_dir_path_for_win
        self.logcat_log_path_for_shell = r'%s/\logcat_log.log' % self.log_dir_path_for_shell
        self.monkey_log_path = r'%s\monkey_log.log' % self.log_dir_path_for_win
        self.device_props_file_path = r'%s\device_props.log' % self.log_dir_path_for_win
        self.app_dump_file_path = r'%s\app_info.log' % self.log_dir_path_for_win

        SysUtils.create_dir_on_win(self.log_dir_path_for_win)
        self.log_manager = LogManager(self.exec_log_path)
        self.logger = self.log_manager.get_logger()
        self.sysutils = SysUtils(self.logger)
        self.adbutils = AdbUtils(self.logger)
        self.monitor = MonkeyMonitor(self.logger)
        
    # --------------------------------------------------------------
    # Build Commands
    # --------------------------------------------------------------
    def __build_monkey_cmd(self):
        monkey_cmd = 'adb shell monkey --throttle 500 -p %s' % self.test_pkg_name

        monkey_launch_params = '-c android.intent.category.MONKEY -c android.intent.category.LAUNCHER -c ' + \
            'android.intent.category.DEFAULT --monitor-native-crashes --kill-process-after-error'
        monkey_ignore = ''
        if Constants.IS_MONKEY_CRASH_IGNORE:
            monkey_ignore = '--ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes'
        monkey_actions_pct = '--pct-touch 75 --pct-motion 10 --pct-trackball 5 --pct-nav 0 ' + \
            '--pct-majornav 5 --pct-syskeys 5 --pct-appswitch 0 --pct-flip 0 --pct-anyevent 0'
        monkey_format = '-v -v -v %s > %s' % (Constants.MONKEY_TOTAL_RUN_TIMES, self.monkey_log_path)

        return ' '.join((monkey_cmd, monkey_launch_params, monkey_ignore, monkey_actions_pct, monkey_format))

    def __build_logcat_cmd(self):
        return 'adb logcat -c && adb logcat -f %s -v threadtime *:%s' % (self.logcat_log_path_for_shell, Constants.LOGCAT_LOG_LEVEL)

    # --------------------------------------------------------------
    # Run Commands
    # --------------------------------------------------------------
    def __run_logcat_subprocess(self):
        return subprocess.Popen(self.__build_logcat_cmd(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def __get_monkey_process_id(self):
        return AdbUtils.get_process_id_by_name('monkey')

    def __get_logcat_process_id(self):
        return AdbUtils.get_process_id_by_name('logcat')

    # --------------------------------------------------------------
    # Functions: IO and report files
    # --------------------------------------------------------------
    def __is_device_busy(self, lines):
        for line in lines:
            if 'busy' in line:
                self.logger.error(line)
                self.logger.error('Error, monkey test exit because of device busy!')
                exit(1)
    
    def __create_log_dir_for_shell(self, dir_path):
        self.__is_device_busy(AdbUtils.create_dir_on_shell(dir_path))
        
    def __remove_testing_log_files_on_device(self):
        self.__is_device_busy(AdbUtils.remove_files_on_shell(self.log_dir_path_for_shell))

    def __pull_all_testing_logs(self):
        # the adb connection maybe disconnect when running the monkey
        if not self.adbutils.is_adb_devices_connect():
            self.logger.warning('Warn, no devices connected, NO files pulled!')
            return
    
        cmd_pull_logcat_log = 'adb pull %s %s' % (self.logcat_log_path_for_shell, self.log_dir_path_for_win)
        self.sysutils.run_sys_cmd(cmd_pull_logcat_log)

        self.adbutils.dump_anr_files(self.log_dir_path_for_win)
        self.adbutils.dump_tombstone_files(self.log_dir_path_for_win)
    
    # --------------------------------------------------------------
    # Monkey Test Main
    # --------------------------------------------------------------
    def __test_setup_main(self):
        # shell env setup
        self.adbutils.clear_anr_dir()
        self.adbutils.clear_tombstone_dir()
        self.__remove_testing_log_files_on_device()
        self.__create_log_dir_for_shell(self.log_dir_path_for_shell)
    
        # win env setup
        self.adbutils.dump_device_props(self.device_props_file_path)
        self.adbutils.dump_app_info(Constants.PKG_NAME_ZGB, self.app_dump_file_path)

    def __test_main(self):
        self.logger.info('Start logcat process.')
        logcat_p = self.__run_logcat_subprocess()
    
        self.logger.info('Start monkey monitor process.')
        monitor_t = threading.Thread(target=self.monitor.process_monkey_monitor_main)
        monitor_t.start()
        self.logger.info('Start to exec monkey process.')
        self.sysutils.run_sys_cmd(self.__build_monkey_cmd())
        monitor_t.join()

        logcat_p.kill()

    def __test_clearup_main(self):
        self.__pull_all_testing_logs()
        self.adbutils.kill_process_by_pid(self.__get_logcat_process_id())
        self.log_manager.clear_log_handles()
    
    def mokeytest_main(self):
        self.__test_setup_main()
        self.__test_main()
        self.__test_clearup_main()
    
    
if __name__ == '__main__':
    
    test = MonkeyTest(Constants.PKG_NAME_ZGB, '1', 1)
    test.mokeytest_main()
    print('Monkey test DONE.')
