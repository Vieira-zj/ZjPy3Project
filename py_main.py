# -*- coding: utf-8 -*-
'''
Created on 2018-11-2

@author: zhengjin
'''

import sys
from monkeytest import AdbUtils
from monkeytest import Constants
from monkeytest import MonkeyTest
from monkeytest import SysUtils


def test_imports():
    '''
    define imports in monkeytest.__init__.py, and import py modules
    '''
    print('test file path:', Constants.TEST_FILE_PATH)
    print('\ncurrent date:', SysUtils.get_current_date())
    print('\nadb info:', AdbUtils.print_adb_info())


def run_monkey_test(args_kv):
    test = MonkeyTest(Constants.PKG_NAME_ZGB, args_kv.get(Constants.RUN_MINS_TEXT, Constants.RUN_MINS))
    test.mokeytest_main()


def cmd_args_parse():

    def usage():
        lines = []
        lines.append('usage:')
        lines.append('  python monkey_test.py [-t 30]')
        lines.append('options:')
        lines.append('  -t: time, monkey test run xx minutes. if not set, use RUN_MINS in constants.py as default.')
        lines.append('  -h: help')
        print('\n'.join(lines))

    import getopt
    opts, _ = getopt.getopt(sys.argv[1:], 'ht:')

    ret_dict = {}
    if len(opts) == 0:
        # print usage and use default monkey test confs.
        usage()
        return ret_dict
    
    for op, value in opts:
        if op == '-t':
            ret_dict.update({Constants.RUN_MINS_TEXT:value})
        elif op == '-h':
            usage()
            exit(0)

    return ret_dict

    
if __name__ == '__main__':
    
#     test_imports()

    args_dict = cmd_args_parse()
    run_monkey_test(args_dict)
    print('Python main DONE.')
