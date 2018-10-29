# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''


class Constants(object):
    '''
    classdocs
    '''

    # test configs
    TEST_FILE_PATH = r'd:\test.txt'
    LOG_FILE_PATH = r'd:\test_log.txt'

    # monkey configs
    MONKEY_TOTAL_RUN_TIMES = '1000000'
    IS_MONKEY_CRASH_IGNORE = True
    MAX_RUN_TIME = 12 * 60 * 60
    WAIT_TIME_IN_LOOP = 60
    LOGCAT_LOG_LEVEL = 'I'

    PKG_NAME_ZGB = 'com.jd.b2b'   

    def __init__(self, params):
        '''
        Constructor
        '''
        
