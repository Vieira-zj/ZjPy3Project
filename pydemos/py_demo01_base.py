# -*- coding: utf-8 -*-
'''
Created on 2018-10-31
@author: zhengjin
'''

import getopt
import glob
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# examle 01, base
def py_base_ex01():
    # test for None
    flagObject = None
    if flagObject:
        print('object is not none.')
    else:
        print('object is none.')

    # test for search str
    def search_by_index(input_str):
        try:
            print(input_str[:input_str.index('g')])
        except ValueError as e:
            print(e)
    search_by_index('16g')
    search_by_index('32')

    def search_by_find(input_str):
        if input_str.find('g') == -1:
            print('search not found')
        else:
            print(input_str[:input_str.find('g')])
    print('')
    search_by_find('16g')
    search_by_find('32')


# example 02, print multiple lines
def py_base_ex02():
    lines = '\n'.join([
        'step1, this is the line one for test;',
        'step2, this is the line two for test;',
        'step3, this is the line three for test.',
    ])
    print(lines)
    print()

    line = ('stepA, this is the line one for test;'
            'stepB, this is the line two for test;'
            'stepC, this is the line three for test.'
            )
    print(lines)


# example 03, import external modules
def py_base_ex03():
    sys.path.append(os.getenv('PYPATH'))

    from utils import Constants
    from utils import LogManager
    from utils import SysUtils

    try:
        logger = LogManager.build_logger(Constants.LOG_FILE_PATH)
        utils = SysUtils().get_instance()
        utils.run_sys_cmd('python --version')
    finally:
        LogManager.clear_log_handles()


# example 04, context current path
# NOTE: context cur_path is the path where run cmd "python [script.py]"
def py_base_ex04():
    cur_path = os.getcwd()
    print('current path:', cur_path)

    f_path = os.path.abspath('../README.md')
    print('file exist check (%s):' % f_path, os.path.exists(f_path))


# example 05, parse command line args
def py_base_ex05():
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


# example 06, chart line
def py_base_ex06():
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


# example 07, chart spot 
def py_base_ex07():
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


# example 08, reg expression
def py_base_ex08():
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


# example 09, list files by glob
def py_base_ex09():
    '''
    get file path by glob (regexp pattern)
    '''

    # "glob.glob" return list
    tmp_dir = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files')
    files = glob.glob(tmp_dir + '/*.txt')
    print('\ntext files in tmp dir:', files)

    files = glob.glob(os.getcwd() + '/*.py')
    print('\npy files in current dir:', files)
    print()

    # "glob.iglob" return generator
    print('\ntext files in tmp dir:')
    for file in glob.iglob(tmp_dir  + '/*.txt'):
        print(file)

    print('\npy files in current dir:')
    for file in glob.iglob(os.getcwd() + '/*.py'):
        print(file)


# example 10, list files in sub dir
def py_base_ex10():
    output_dir = os.path.join(os.getenv('PYPATH'), 'apitest/outputs')
    
    # list subdirs and files in dir, depth=1, ret name
    print('\nresult files in outputs: ')
    for file in os.listdir(output_dir):
        print(file)

    # list files by glob, depth=2, ret abs path
    files = glob.glob(output_dir + '/*')
    files.extend(glob.glob(output_dir + '/*/*'))
    print('\nresult files in outputs by glob regexp: ')
    for file in files:
        if os.path.isfile(file):
            print('/' + file[file.find('outputs'):])
    print('total files:', len(files))

    # list files by walk, depth=max
    print('\nresult files in outputs by walk:')
    total = 0
    for dir_path, subpaths, files in os.walk(output_dir):
        for file in files:
            print(os.path.join(dir_path, file))
        total = total + len(files)
    print('total files:', total)


# example 11, collections deque
def py_base_ex11():
    import collections

    names = ['jack', 'leo', 'sam', 'peter', 'jeo']
    deque_names = collections.deque(names)
    deque_names.popleft()
    deque_names.appendleft('mark')
    print(deque_names)


# example 12, get sum of each color
def py_base_ex12():
    colors = ['red', 'green', 'red', 'blue', 'green', 'red']

    tmp_dict01 = {}
    for color in colors:
        tmp_dict01.setdefault(color, 0)
        tmp_dict01[color] += 1
    print(tmp_dict01)

    tmp_dict02 = {}
    for color in colors:
        tmp_dict02[color] = tmp_dict02.get(color, 0) + 1
    print(tmp_dict02)


# example 13, default dict
def py_base_ex13():
    names = ['jack', 'leo', 'sam', 'peter', 'jeo']

    from collections import defaultdict
    # set dict value default as list
    tmp_dict = defaultdict(list)
    for name in names:
        key = len(name)
        tmp_dict[key].append(name)
    print(tmp_dict)


# example 14, create dict from lists
def py_base_ex14():
    tmp_lst_ks = ['k1', 'k2', 'k3']
    tmp_lst_vs = ['v1', 'v2', 'v3']

    for k, v in zip(tmp_lst_ks, tmp_lst_vs):
        print('%s=%s' % (k, v))

    tmp_dict = dict([(k.upper(), v.upper()) for k, v in zip(tmp_lst_ks, tmp_lst_vs)])
    print('%s: %s' % (type(tmp_dict), tmp_dict))
    print()

    tmp_dict = {k.upper(): v.upper() for k, v in zip(tmp_lst_ks, tmp_lst_vs)}
    print('%s: %s' % (type(tmp_dict), tmp_dict))


# example 15, iterator by diff step
def py_base_ex15():
    alist = []
    for i in range(10):
        alist.append(i)
    print(alist)

    alist.clear()
    for i in range(10)[::-1]:
        alist.append(i)
    print(alist)

    alist.clear()
    for i in range(10)[::2]:
        alist.append(i)
    print(alist)


# example 16, pass var by value / reference
def py_base_ex16():
    def update_num(number):  # pass value
        number += 5

    def update_num_dict(number_dict):  # pass reference
        number_dict['value'] += 5

    def update_list(alist):  # pass reference
        alist.append(1)
        alist = [1, 2]

    number = 10
    update_num(number)
    print('number:', number)

    number_dict = {'value': 10}
    update_num_dict(number_dict)
    print('number value:', number_dict['value'])

    alist = []
    update_list(alist)
    print('list:', alist)


# example 17, decorator for class function
def py_base_ex17():
    def verify_dir_path(func):
        def _deco(*args, **kwargs):
            print('verify_dir_path args:', args)
            this = args[0]
            if not os.path.exists(this._dir_path):
                raise FileNotFoundError('dir path is not exist!')
            if not os.path.isdir(this._dir_path):
                raise IOError('dir path is not invalid!')
            return func(*args, **kwargs)

        return _deco

    class ListFile(object):
        def __init__(self, dir_path):
            self._dir_path = dir_path

        @verify_dir_path
        def listTextFiles(self):
            files = glob.glob(self._dir_path + '/*.txt')
            print('text files:', files)

        @verify_dir_path
        def listYmlFiles(self):
            files = glob.glob(self._dir_path + '/*.yml')
            print('yml files:', files)

    list_file = ListFile(os.path.join(os.getenv('HOME'), 'Downloads/tmp_files'))
    list_file.listTextFiles()
    list_file.listYmlFiles()


# example 18, *args
def py_base_ex18():
    test_lst = ['a', 'b', 'c']

    def print_abc(a, b, c):
        print(f'a={a}, b={b}, c={c}')
    print_abc(*test_lst)

    def print_vals(*args):
        print('type:', type(args))
        print(f'input arguments: {args}')
    print_vals(test_lst)
    print_vals(*test_lst)


# example 19, json parse
def py_base_ex19():
    import json

    input_path = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/test.json')
    if not os.path.exists(input_path):
        raise FileNotFoundError(input_path)

    json_text = ''
    with open(input_path) as f:
        json_text = f.read()

    if len(json_text) > 0:
        json_object = json.loads(json_text)
        print('request id:', json_object['requestId'])
        print('instance job:', json_object['rawInstances'][0]['rawFeatures']['job'])


# example 20, 写入中文到文件
def py_base_ex20():
    file_path = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/test.file')

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, 'a', encoding='utf-8') as f:
        lines = ['\npython test write chinese words.\n']
        lines.append('写入中文到文件测试1\n')
        f.writelines(lines)
        f.write('写入中文到文件测试2\n')


# example 21, multi process
def py_base_ex21():
    import time
    from multiprocessing import Process

    class MyProcess(Process):
        def __init__(self, tag):
            self._tag = tag
            super().__init__()  # super.init() should be invoked

        def run(self):
            print('%s => pid=%d, name=%s is running ...' % (self._tag, os.getpid(), self.name))
            time.sleep(3)

    p = MyProcess('test')
    print('process start')
    p.start()

    print('main=%d, wait for process done' % os.getpid())
    p.join(timeout=3)
    time.sleep(1)
    if p.is_alive():
        p.kill()


if __name__ == '__main__':

    py_base_ex21()

    print('PYPATH='+os.getenv('PYPATH') if len(os.getenv('PYPATH')) > 0 else 'PYPATH=null')
    print('\npython version:\n', sys.version)
    print('python base demo DONE.')
