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
    # (Touch events are a down-up event in a single place on the screen.)
    PCT_TOUCH = '60'
    # (Motion events consist of a down event somewhere on the screen, a series of pseudo-random movements, and an up event.)
    PCT_MOTION = '20'
    # (Trackball events consist of one or more random movements, sometimes followed by a click.)
    PCT_TRACKBALL = '5'
    # (Navigation events consist of up/down/left/right, as input from a directional input device.)
    PCT_NAV = '0'
    # (These are navigation events that will typically cause actions within your UI, such as the center button in a 5-way pad, the back key, or the menu key.)
    PCT_MAJORNAV = '5'
    # (These are keys that are generally reserved for use by the system, such as Home, Back, Start Call, End Call, or Volume controls.)
    PCT_SYSKEYS = '5'
    # At random intervals, the Monkey will issue a startActivity() call, as a way of maximizing coverage of all activities within your package.
    PCT_APPSWITCH = '5'
    # This is a catch-all for all other types of events such as keypresses, other less-used buttons on the device, and so forth.
    PCT_ANYEVENT = '0'
    
    IS_MONKEY_CRASH_IGNORE = True
    MONKEY_TOTAL_RUN_TIMES = '1000000'

    MAX_RUN_TIME = 12 * 60 * 60
    WAIT_TIME_IN_LOOP = 15
    LOGCAT_LOG_LEVEL = 'I'

    PKG_NAME_ZGB = 'com.jd.b2b'
    RUN_MINS_TEXT = 'run_mins'
    RUN_MINS = 3
    
    IS_PROFILE_TEST = False
    ITEST_COLLECT_INTERVAL = 3
    IS_CREATE_ARCHIVE = False

    def __init__(self, params):
        '''
        Constructor
        '''


if __name__ == '__main__':

    pass
