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
        self.logger = logger

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
        self.logger.debug('Exec command: %s' % cmd)
        ret = os.system(cmd)
        if not ret == 0:
            self.logger.warning('Failed, run command => %s, return code is %d' % (cmd, ret))
            return False
        return True
    
    def run_sys_cmd_and_ret_lines(self, cmd):
        self.logger.debug('Exec command: %s' % cmd)
        lines = os.popen(cmd).readlines()
        if len(lines) == 0:
            self.logger.warning('The output is null for command => %s' % cmd)
        return lines

    def run_sys_cmd_and_ret_content(self, cmd):
        self.logger.debug('Exec command: %s' % cmd)
        content = os.popen(cmd).read()
        if content is None or content == '':
            self.logger.warning('The output is null for command => %s' % cmd)
            content = ''
        return content

    def run_sys_cmd_in_subprocess(self, cmd):
        self.logger.debug('Exec command: %s' % cmd)
    
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
    
        lines_error = p.stderr.readlines()
        lines_output = p.stdout.readlines()
        if len(lines_error) > 0:
            return lines_error
        if len(lines_output) > 0:
            return lines_output
        self.logger.warning('The output is null for command => %s' % cmd)
        return ''

    # --------------------------------------------------------------
    # IO function
    # --------------------------------------------------------------    
    @classmethod
    def create_dir_on_win(cls, path):
        if os.path.exists(path):
            return
        os.makedirs(path)

    def write_content_to_file(self, file_path, content, is_override=True):
        if len(content) == 0:
            self.logger.error('The input content is empty!')
            return
        
        if os.path.exists(file_path):
            if is_override:
                self.logger.info('The file(%s) is exist, and the content will be override!' % file_path)
            else:
                self.logger.error('The file(%s) is exist!' % file_path)
                return
            
        with codecs.open(file_path, 'w', 'utf-8') as f:
            f.write(content)
            f.flush()


if __name__ == '__main__':

    from log_manager import LogManager
    from constants import Constants

    logger = LogManager(Constants.LOG_FILE_PATH).get_logger()
    utils = SysUtils(logger)
    utils.run_sys_cmd('python -V')
    utils.write_content_to_file(Constants.TEST_FILE_PATH, 'test')
    print('system utils test DONE!')
