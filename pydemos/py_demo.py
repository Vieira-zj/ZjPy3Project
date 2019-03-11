# -*- coding: utf-8 -*-
'''
Created on 2018-10-31

@author: zhengjin
'''

import getopt
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def import_utils_lib_test():
    sys.path.append(os.getenv('PYPATH'))

    from utils import Constants
    from utils import LogManager
    from utils import SysUtils

    manager = LogManager(Constants.LOG_FILE_PATH)
    try:
        logger = manager.get_logger()
        utils = SysUtils(logger)
        utils.run_sys_cmd('python --version')
    finally:
        if manager is not None:
            manager.clear_log_handles()


def cmd_args_parse():
    # "hi:o:": h => -h, i: => -i input_file, o: => -o output_file
    opts, _ = getopt.getopt(sys.argv[1:], 'hi:o:')

    if len(opts) == 0:
        usage()
        exit(0)

    input_file = ''
    output_file = ''
    for op, value in opts:
        if op == '-i':
            input_file = value
        elif op == '-o':
            output_file = value
        elif op == '-h':
            usage()
            exit(0)
    print('input file: %s, output file: %s' % (input_file, output_file))


def usage():
    lines = []
    lines.append('usage:')
    lines.append('-i: input file')
    lines.append('-o: output file')
    lines.append('-h: help')
    print('\n'.join(lines))


def chart_line_demo():
    '''
    pre-conditions: 
    $ pip install numpy
    $ pip install matplotlib
    '''
    print('numpy version: ' + np.__version__)
    print('matplotlib version: ' + matplotlib.__version__)

    import matplotlib.pyplot as plt

    x_arr = [x for x in range(0, 10)]
    y_arr = [y for y in range(0, 20) if y % 2 == 0]
    z_arr = [y for y in range(0, 20) if y % 2 != 0]

    plt.title('Chart Test')
    ave_desc = 'y average: %d, z average: %d' % (np.average(y_arr), np.average(z_arr))
    plt.xlabel('X_label_text\n green: system_cpu, blue: user_cpu\n' + ave_desc)
    plt.ylabel('Y_label_text')

    plt.plot(x_arr, y_arr, color='red')
    plt.plot(x_arr, z_arr, color='blue')
    plt.grid(True, color='green', linestyle='--', linewidth='1')

    # plt.show()

    # default pixel [6.0,4.0]
    # if set dpi=100, image size 600*400
    # if set dpi=200, image size 1200*800
    # if set dpi=300，image size 1800*1200

    plt.tight_layout()
    plt.savefig(r'd:\profile.png', format='png', dpi=300)
    plt.close()


def chart_spot_demo():
    # data
    # y_arr = [float(y) for y in range(0, 100) if y % 2 == 0]
    # x_arr = [x for x in range(0, len(y_arr))]

    n = 1024
    # 均值为0, 方差为1的随机数
    x_arr = np.random.normal(0, 1, n)
    y_arr = np.random.normal(0, 1, n)

    # 计算颜色值
    color = np.arctan2(x_arr, y_arr)
    # 绘制散点图
    plt.scatter(x_arr, y_arr, s=30, c=color, alpha=0.5)

    # 设置坐标轴范围
    plt.xlim((0, max(x_arr)))
    plt.ylim((0, max(y_arr)))

    # 不显示坐标轴的值
    plt.xticks(())
    plt.yticks(())

    plt.show()


def regexp_demo():
    '''
    Get Java exceptions sum info from input content.
    '''
    input_lines = []
    input_lines.append(
        'W System.err: org.json.JSONException: No value for preSaleSkuInfo')
    input_lines.append(
        'W System.err: Attempt to invoke virtual method \'int java.lang.String.length()\' on a null object reference')
    input_lines.append(
        'W System.err: net.grandcentrix.tray.core.TrayException: could not access stored data with uri')
    input_lines.append(
        'W System.err: org.json.JSONException: No value for preSaleSkuInfo')

    import re
    ret_dict = {}
    for line in input_lines:
        re_results = re.match('.*:\s+(.*Exception.{20,30})', line)
        exception_key = ''
        try:
            exception_key = re_results.group(1)
        except AttributeError as e:
            print(e)
            continue

        tmp_val = 0
        try:
            tmp_val = ret_dict[exception_key]
            ret_dict[exception_key] = tmp_val + 1
        except KeyError as e:
            print(e)
            ret_dict[exception_key] = 1

    print(ret_dict)


def file_search():
    '''
    get file path by regexp pattern
    '''
    import glob

    # "glob.glob" return list
    tmp_dir = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/*.txt')
    files = glob.glob(tmp_dir)
    print('\ntext files in tmp dir:', files)

    cur_dir = './*.py'
    files = glob.glob(cur_dir)
    print('\npy files in current dir:', files)

    # "glob.iglob" return generator
    print('\ntext files in tmp dir:')
    for file in glob.iglob(tmp_dir):
        print(file)

    print('\npy files in current dir:')
    for file in glob.iglob(cur_dir):
        print(file)


if __name__ == '__main__':

    # import_utils_lib_test()
    # cmd_args_parse()

    # chart_line_demo()
    # chart_spot_demo()

    # regexp_demo()
    # file_search()

    # NOTE: context cur_path is the path where run "python" cmd
    f_path = os.path.abspath('../README.md')
    print('file check (%s):' % f_path, os.path.exists(f_path))

    print('python demo DONE.')
