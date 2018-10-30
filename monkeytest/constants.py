# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''


class Constants(object):
    '''
    classdocs
    '''

    # test conf
    TEST_FILE_PATH = r'd:\test.txt'
    LOG_FILE_PATH = r'd:\test_log.txt'

    # monkey conf
    MONKEY_TOTAL_RUN_TIMES = '1000000'
    IS_MONKEY_CRASH_IGNORE = True

    MAX_RUN_TIME = 12 * 60 * 60
    WAIT_TIME_IN_LOOP = 15
    LOGCAT_LOG_LEVEL = 'I'

    PKG_NAME_ZGB = 'com.jd.b2b'   
    RUN_MINS = 10

    def __init__(self, params):
        '''
        Constructor
        '''


if __name__ == '__main__':

    import re
    test_str = 'list: device offline'
    if re.search('unknown|offline', test_str):
        print('error')
    else:
        print('success')

    print('test DONE.')
