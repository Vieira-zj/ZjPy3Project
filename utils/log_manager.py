# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''

import logging
import sys
sys.path.append('../')

from utils import Constants


class LogManager(object):
    '''
    classdocs
    '''

    __manager = None
    __log_path = ''

    @classmethod
    def get_instance(cls):
        if cls.__manager is None:
            raise RuntimeError('log manager is not init!')
        return cls.__manager

    @classmethod
    def biuld(cls, log_path):
        if len(log_path) == 0:
            raise ValueError('log path is null!')
        cls.__manager = LogManager(log_path)
        return cls

    def __init__(self, log_path, basic_log_level=logging.DEBUG, file_log_level=logging.INFO):
        '''
        兼容老的调用方式
        '''
        self.__log_path = log_path
        self.__basic_log_level = basic_log_level
        self.__file_log_level = file_log_level
        self.__logger = None

    def get_logger(self):
        if self.__logger is None:
            self.__build_logger()
        return self.__logger

    def __build_logger(self):
        log_format_long = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
        log_format_short = '%(filename)s: [%(levelname)s] >>> %(message)s'
        date_format_long = '%a, %d %b %Y %H:%M:%S'
        date_format_short = '%d %b %H:%M:%S'

        # log main handler
        logging.basicConfig(level=self.__basic_log_level,
                            format=log_format_short, datefmt=date_format_short)

        # set file handler
        # note: file_log_level > basic_log_level
        fh = logging.FileHandler(
            filename=self.__log_path, mode='w', encoding='utf-8')
        fh.setFormatter(logging.Formatter(fmt=log_format_long, datefmt=date_format_long))
        fh.setLevel(self.__file_log_level)

        self.__logger = logging.getLogger()
        self.__logger.addHandler(fh)

    def clear_log_handles(self):
        if self.__logger.hasHandlers():
            for fh in self.__logger.handlers:
                fh.close()
# end class


def sub_process(logger):
    import time
    time.sleep(1)
    print('in sub process')
    logger.info('info message test in sub process')


if __name__ == '__main__':

    import multiprocessing
    import threading

    manager = LogManager.biuld(Constants.LOG_FILE_PATH).get_instance()
    logger = manager.get_logger()
    logger.debug('debug message test')
    logger.info('info message test')
    logger.warning('warning message test')

    # note: log from logging only print in thread but not process
    p1 = multiprocessing.Process(name='test_process', target=sub_process, args=(logger,))
    p1.start()
    p1.join()
    logger.info('process %s done' % p1.name)

    p2 = threading.Thread(name='test_thread', target=sub_process, args=(logger,))
    p2.start()
    p2.join()
    logger.info('process %s done' % p2.name)

    LogManager.get_instance().get_logger().info('log utils test DONE.')
    manager.clear_log_handles()
