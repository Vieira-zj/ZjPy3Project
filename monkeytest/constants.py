# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''


class Constants(object):
    '''
    classdocs
    '''

    TEST_FILE_PATH = r'd:\test.txt'

    # log configs
    LOG_FILE_PATH = r'd:\test_log.txt'

    # monkey configs
    PKG_NAME_ZGB = 'com.jd.b2b'   
    MONKEY_TOTAL_RUN_TIMES = '1000000'
    IS_MONKEY_CRASH_IGNORE = True
    MAX_RUN_TIME = 12 * 60 * 60
    WAIT_TIME_IN_LOOP = 60
    
    LOGCAT_LOG_LEVEL = 'I'

    def __init__(self, params):
        '''
        Constructor
        '''
        
