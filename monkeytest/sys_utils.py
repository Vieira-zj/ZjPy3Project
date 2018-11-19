# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''

import codecs
import os
import subprocess
import time


class SysUtils(object):
    '''
    classdocs
    '''

    def __init__(self, logger):
        '''
        Constructor
        '''
        self.__logger = logger

    # --------------------------------------------------------------
    # Time functions
    # --------------------------------------------------------------
    @classmethod
    def get_current_date_and_time(cls):
        return time.strftime('%y-%m-%d_%H%M%S')

    @classmethod
    def get_current_date(cls):
        return time.strftime('%Y%m%d')

    # --------------------------------------------------------------
    # Run system commands
    # --------------------------------------------------------------    
    def run_sys_cmd(self, cmd):
        self.__logger.debug('Exec command: %s' % cmd)
        ret = os.system(cmd)
        if not ret == 0:
            self.__logger.warning('Failed, run command => %s, return code is %d' % (cmd, ret))
            return False
        return True
    
    def run_sys_cmd_and_ret_lines(self, cmd):
        self.__logger.debug('Exec command: %s' % cmd)
        lines = os.popen(cmd).readlines()
        if len(lines) == 0:
            self.__logger.warning('The output is null for command => %s' % cmd)
        return lines

    def run_sys_cmd_and_ret_content(self, cmd):
        self.__logger.debug('Exec command: %s' % cmd)
        content = os.popen(cmd).read()
        if content is None or content == '':
            self.__logger.warning('The output is null for command => %s' % cmd)
            content = ''
        return content.strip('\r\n')

    def run_sys_cmd_in_subprocess(self, cmd):
        self.__logger.debug('Exec command: %s' % cmd)
    
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
    
        lines_error = p.stderr.readlines()
        lines_output = p.stdout.readlines()
        if len(lines_error) > 0:
            return lines_error
        if len(lines_output) > 0:
            return lines_output
        self.__logger.warning('The output is null for command => %s' % cmd)
        return ''

    # --------------------------------------------------------------
    # IO function
    # --------------------------------------------------------------    
    @classmethod
    def create_dir_on_win(cls, path):
        if os.path.exists(path):
            return
        os.makedirs(path)

    @classmethod
    def delete_files_in_dir(cls, dir_path):
        if not os.path.exists(dir_path):
            return
        import shutil
        shutil.rmtree(dir_path)

    def write_content_to_file(self, file_path, content, is_override=True):
        if len(content) == 0:
            self.__logger.error('The input content is empty!')
            return
        
        if os.path.exists(file_path):
            if is_override:
                self.__logger.info('The file(%s) is exist, and the content will be overrided!' % file_path)
            else:
                self.__logger.error('The file(%s) is exist!' % file_path)
                return
            
        with codecs.open(file_path, 'w', 'utf-8') as f:
            f.write(content)
            f.flush()


if __name__ == '__main__':

#     SysUtils.delete_files_in_dir(r'D:\JDTestLogs\handTest')
    
    from monkeytest.constants import Constants
    from monkeytest.log_manager import LogManager
 
    manager = LogManager(Constants.LOG_FILE_PATH)
    logger = manager.get_logger()
    utils = SysUtils(logger)
    utils.run_sys_cmd('python -V')
    utils.write_content_to_file(Constants.TEST_FILE_PATH, 'test')
    manager.clear_log_handles()
    
    print('system utils test DONE.')
