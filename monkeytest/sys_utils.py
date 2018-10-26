# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''

import os
import subprocess
from log_manager import LogManager


class SysUtils(object):
    '''
    classdocs
    '''

    logger = LogManager.getLoggerInstance()

    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    @classmethod
    def run_sys_cmd(cls, cmd):
        cls.logger.debug('Run command: %s' % cmd)
        ret = os.system(cmd)
        if not ret == 0:
            cls.logger.warning('Failed, run command => %s, return code is %d' % (cmd, ret))
            return False
        return True
    
    @classmethod
    def run_sys_cmd_and_ret_lines(cls, cmd):
        cls.logger.debug('Run command: %s' % cmd)
        lines = os.popen(cmd).readlines()
        if len(lines) == 0:
            cls.logger.warning('The output is null for command => %s' % cmd)
        return lines

    @classmethod
    def run_sys_cmd_and_ret_content(cls, cmd):
        cls.logger.debug('Run command: %s' % cmd)
        content = os.popen(cmd).read()
        if content is None or content == '':
            cls.logger.warning('The output is null for command => %s' % cmd)
            content = ''
        return content

    @classmethod
    def run_sys_cmd_in_subprocess(cls, cmd):
        cls.logger.debug('Run command: %s' % cmd)
    
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
    
        lines_error = p.stderr.readlines()
        lines_output = p.stdout.readlines()
        if len(lines_error) > 0:
            return lines_error
        if len(lines_output) > 0:
            return lines_output
        cls.logger.warning('The output is null for command => %s' % cmd)
        return ''


if __name__ == '__main__':

    SysUtils.run_sys_cmd('python -V')    
    print('system utils test DONE!')
