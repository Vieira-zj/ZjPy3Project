# -*- coding: utf-8 -*-
'''
Created on 2018-11-2

@author: zhengjin
'''


def test_imports():
    '''
    define imports in monkeytest.__init__.py, and import py modules
    '''
    from monkeytest import Constants
    print('test file path:', Constants.TEST_FILE_PATH)

    from monkeytest import SysUtils
    print('\ncurrent date:', SysUtils.get_current_date())

    from monkeytest import AdbUtils
    print('\nadb info:', AdbUtils.print_adb_info())

    
if __name__ == '__main__':
    
    test_imports()
