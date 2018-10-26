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

    logger = None

    @classmethod
    def getLoggerInstance(cls, basic_log_level=logging.DEBUG, file_log_level=logging.INFO):
        if len(Constants.LOG_FILE_PATH) == 0:
            raise Exception('log file path is not set in properties before get logger instance!')
        if cls.logger is not None:
            return cls.logger
        
        cls.logger = LogManager().__init_log_config(basic_log_level, file_log_level)
        return cls.logger

    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def __init_log_config(self, basic_log_level, file_log_level):
        log_format_long = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
        log_format_short = '%(filename)s: [%(levelname)s] >>> %(message)s'
        date_format_long = '%a, %d %b %Y %H:%M:%S'
        date_format_short = '%d %b %H:%M:%S'
    
        # log main handler
        logging.basicConfig(level=basic_log_level, format=log_format_short, datefmt=date_format_short)
    
        # set file handler
        # note: file_log_level > basic_log_level
        fh = logging.FileHandler(filename=Constants.LOG_FILE_PATH, mode='w', encoding='utf-8')
        fh.setFormatter(logging.Formatter(fmt=log_format_long, datefmt=date_format_long))
        fh.setLevel(file_log_level)

        self.logger = logging.getLogger()
        self.logger.addHandler(fh)
        self.logger.debug('init logger config')
        return self.logger

        
if __name__ == '__main__':

#     logger = LogManager().init_log_config(logging.DEBUG, logging.INFO)
    logger = LogManager.getLoggerInstance()

    logger.debug('debug message test')
    logger.info('info message test')
    logger.warning('warning message test')
    
    print('log utils test DONE!')
