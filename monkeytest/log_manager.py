# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''

import logging
from constants import Constants


class LogManager(object):
    '''
    classdocs
    '''

    def __init__(self, log_path, basic_log_level=logging.DEBUG, file_log_level=logging.INFO):
        '''
        Constructor
        '''
        self.basic_log_level = basic_log_level
        self.file_log_level = file_log_level
        self.log_path = log_path
        
    def get_logger(self):
        log_format_long = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
        log_format_short = '%(filename)s: [%(levelname)s] >>> %(message)s'
        date_format_long = '%a, %d %b %Y %H:%M:%S'
        date_format_short = '%d %b %H:%M:%S'
    
        # log main handler
        logging.basicConfig(level=self.basic_log_level, format=log_format_short, datefmt=date_format_short)
    
        # set file handler
        # note: file_log_level > basic_log_level
        fh = logging.FileHandler(filename=self.log_path, mode='w', encoding='utf-8')
        fh.setFormatter(logging.Formatter(fmt=log_format_long, datefmt=date_format_long))
        fh.setLevel(self.file_log_level)

        self.logger = logging.getLogger()
        self.logger.addHandler(fh)
        self.logger.debug('init logger config')
        return self.logger


if __name__ == '__main__':

    logger = LogManager(Constants.LOG_FILE_PATH).get_logger()
    logger.debug('debug message test')
    logger.info('info message test')
    logger.warning('warning message test')

    print('log utils test DONE!')
