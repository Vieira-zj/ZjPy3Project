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

print('python base demo INIT.')


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

    lines = ('stepA, this is the line one for test;'
             'stepB, this is the line two for test;'
             'stepC, this is the line three for test.'
             )
    print(lines)

    # print random float number within range
    import random
    f = float('%.1f' % random.choice(np.arange(-2.0, 2.0, step=0.1)))
    print('float number with 1 decimal:', f)
    f = float('%.3f' % random.choice(np.arange(92., 94., step=0.001)))
    print('float number with 3 decimal:', f)


# example 03, import external modules
def py_base_ex03():
    sys.path.append(os.getenv('PYPATH'))

    from utils import Constants
    from utils import LogManager
    from utils import SysUtils

    try:
        logger = LogManager.build_logger(Constants.LOG_FILE_PATH)
        logger.info('import external modules test.')
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
    ave_desc = 'y average: %d, z average: %d' % (
        np.average(y_arr), np.average(z_arr))
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


# example 08_01, re.match() and re.search()
def py_base_ex08_01():
    import re

    print(re.match('super', 'superstition').span())  # (0, 5)
    print(re.match('super', 'insuperable'))  # None

    print(re.search('super', 'superstition').span())  # (0, 5)
    print(re.search('super', 'insuperable').span())  # (2, 7)


# example 08_02, reg exp
def py_base_ex08_02():
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
        re_results = re.match(r'.*:\s+(.*Exception.{20,30})', line)
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
    for file in glob.iglob(tmp_dir + '/*.txt'):
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
    # for dir_path, subpaths, files in os.walk(output_dir):
    for dir_path, _, files in os.walk(output_dir):
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

    tmp_dict = dict([(k.upper(), v.upper())
                     for k, v in zip(tmp_lst_ks, tmp_lst_vs)])
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

    list_file = ListFile(os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files'))
    list_file.listTextFiles()
    list_file.listYmlFiles()


# example 18, *args
def py_base_ex18():
    test_lst = ['a', 'b', 'c']

    # as input
    def print_abc(a, b, c):
        print(f'a={a}, b={b}, c={c}')
    print_abc(*test_lst)

    # as args
    def print_vals(*args):
        print('type:', type(args))
        print(f'input arguments: {args}')
    print_vals(1, 2, 3)
    print_vals(test_lst)
    print_vals(*test_lst)


# example 19, json parse
def py_base_ex19():
    import json

    input_path = os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files/test.json')
    if not os.path.exists(input_path):
        raise FileNotFoundError(input_path)

    json_text = ''
    with open(input_path) as f:
        json_text = f.read()

    if len(json_text) > 0:
        json_object = json.loads(json_text)
        print('request id:', json_object['requestId'])
        print('instance job:',
              json_object['rawInstances'][0]['rawFeatures']['job'])


# example 20, 写入中文到文件
def py_base_ex20():
    file_path = os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files/test.file')

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
            print('%s => pid=%d, name=%s is running ...' %
                  (self._tag, os.getpid(), self.name))
            time.sleep(3)

    p = MyProcess('test')
    print('process start')
    p.start()

    print('main=%d, wait for process done' % os.getpid())
    p.join(timeout=3)
    time.sleep(1)
    if p.is_alive():
        p.kill()


# example 22, py tips
def py_base_ex22():
    # 序列解包
    def tip_test01():
        user_ls = ['henry', 18, 'male']
        name, age, gender = user_ls
        print('name=%s, age=%d, male=%s' % (name, age, gender))
    tip_test01()

    # 判断是否为空列表，空字典，空字符串
    def tip_test02():
        l, d, s = [1, 2, 3], {}, ''
        if l:
            print('list is not empty')
        if d:
            print('dict is not empty')
        if s:
            print('string is not empty')
    tip_test02()

    # 判断诸多条件是否至少有一个成立
    def tip_test03():
        math, physics, computer = 70, 40, 80
        if any([math < 60, physics < 60, computer < 60]):
            print('not pass')
    tip_test03()

    # 判断诸多条件是否全部成立
    def tip_test04():
        math, physics, computer = 70, 70, 80
        if all([math >= 60, physics >= 60, computer >= 60]):
            print('pass')
    tip_test04()

    # 过滤数字并求和
    def tip_test05():
        lst = [1, 2, 3, 'a', 'b', 4, 5.0]
        count = sum([i for i in lst if type(i) in (int, float)])
        print('count = %.1f' % count)
    tip_test05()


# example 23_01, print process
def py_base_ex23_01():
    import time
    i, n = 0, 100
    for i in range(n):
        time.sleep(0.1)
        if (i + 1) % 10 == 0:
            print(str(i + 1) + '%', end='\r')


# example 23_02, print progress bar
def py_base_ex23_02():
    def process_bar(num, total):
        rate = float(num) / total
        rate_num = int(100 * rate)
        r = '\r[%s%s]%d' % (
            ('*' * rate_num), (' ' * (100 - rate_num)), rate_num)
        sys.stdout.write(r + '%')
        sys.stdout.flush()

    import time
    i, n = 0, 100
    for i in range(n):
        time.sleep(0.1)
        process_bar(i + 1, n)


# example 24, value and reference
def py_base_ex24():
    # 1 list
    def update_list(lst):
        lst[2] = 30
        print("[update]", lst)

    lst = [1, 2, 3, 4, 5]
    print("\nsrc list:", lst)

    lst2 = lst
    lst[0] = 10
    lst2[1] = 20
    update_list(lst)
    print("lst: %r, lst2: %r" % (lst, lst2))

    # 2 map
    def update_map(m):
        m[3] = "THREE"
        print("[update]", m)

    m = {1: "one", 2: "two", 3: "three"}
    print("\nsrc map:", m)

    m2 = m
    m[1] = "ONE"
    m2[2] = "TWO"
    update_map(m)
    print("map: %r, map2: %r" % (m, m2))

    # 3 object
    class person(object):
        def __init__(self, name, age, job):
            self.name = name
            self.age = age
            self.job = job

        def __str__(self):
            return "name=%s, age=%d, job=%s" % (self.name, self.age, self.job)

    def update_person(person):
        person.job = "TESTER"
        print("[update]", person)

    p = person("Henry", 30, "tester")
    print("\nsrc person:", p)

    p1 = p
    p.name = "HENRY"
    p1.age += 1
    update_person(p)
    print("p: %s, p1:%s" % (p, p1))


# example 25, datetime
def py_base_ex25():
    import datetime
    from datetime import datetime as dt

    def print_next_day(timestamp):
        next_day_timestamp = timestamp + datetime.timedelta(days=1)
        next_date = dt.strftime(next_day_timestamp, '%Y-%m-%d')
        print(next_date)

    print('\ntomorrow date:')
    now_timestamp = dt.now()
    print_next_day(now_timestamp)
    print('next day for 20190831:')
    test_timestamp = dt.strptime('20190831', '%Y%m%d')
    print_next_day(test_timestamp)

    def print_days(s_date, e_date):
        s_date_timestamp = dt.strptime(s_date, '%Y-%m-%d')
        e_date_timestamp = dt.strptime(e_date, '%Y-%m-%d')
        while s_date_timestamp <= e_date_timestamp:
            print("day:", dt.strftime(s_date_timestamp, '%Y%m%d'))
            s_date_timestamp += datetime.timedelta(days=1)

    print('\ndays between 2019-08-27 and 2019-09-02:')
    print_days('2019-08-27', '2019-09-02')


# example 26, 2d array by numpy
def py_base_ex26():
    array_2d = np.zeros((2, 5))
    for i in range(5):
        array_2d[0][i] = i
    print(array_2d)


# example 27, field type hint
def py_base_ex2701():
    def addTwo(x: int) -> int:
        return x+2
    print('results:', addTwo(10))


def py_base_ex2702():
    import pprint
    from typing import List

    Vector = List[float]
    Matrix = List[Vector]

    def addMatrix(a: Matrix, b: Matrix) -> Matrix:  # type hint
        result = []
        for i, row in enumerate(a):
            result_row = []
            for j, row in enumerate(row):
                result_row += [a[i][j] + b[i][j]]  # instead of list.append()
            result += [result_row]
        return result

    x = [[1.0, 2.0], [3.0, 4.0]]
    y = [[2.0, 2.0], [-3.0, -3.0]]
    res = addMatrix(x, y)
    print('print:', res)
    pprint.pprint(res)  # print复杂对象


# example 28, 类装饰器
def py_base_ex28():
    import functools

    class MyLogging(object):
        def __init__(self, level='warn'):
            self.level = level

        def __call__(self, func):
            @functools.wraps(func)
            def _deco(*args, **kwargs):
                if self.level == 'warn':
                    self.notify(func)
                return func(*args, **kwargs)
            return _deco

        def notify(self, func):
            print('%s is running' % func.__name__)

    @MyLogging(level='warn')  # 执行__call__方法
    def bar(a, b):
        print('i am bar: %d' % (a+b))

    bar(1, 2)


# example 29, iterator and generator
def py_base_ex29():
    from collections.abc import Iterable, Iterator

    mylist = ['a', 'b', 'c']
    print('isinstance(mylist, Iterable):', isinstance(mylist, Iterable))
    print('isinstance(mylist, Iterator):', isinstance(mylist, Iterator))

    myiter = iter(mylist)
    print('\nmyiter:', myiter)
    print('isinstance(myiter, Iterable):', isinstance(myiter, Iterable))
    print('isinstance(myiter, Iterator):', isinstance(myiter, Iterator))

    mygen = (x for x in mylist)
    print('\nmygen:', mygen)
    print('isinstance(mygen, Iterable):', isinstance(mygen, Iterable))
    print('isinstance(mygen, Iterator):', isinstance(mygen, Iterator))

    # file is both iterable and iterator
    with open('data/data.log', mode='r', encoding='UTF-8') as f:
        print('\nfile:', f)
        print('isinstance(f, Iterable):', isinstance(f, Iterable))
        print('isinstance(f, Iterator):', isinstance(f, Iterator))

        print('\nfile content:')
        for line in f:
            print(line.rstrip('\n'))


# example 30, py tips
def py_base_ex30():
    # decimal
    from decimal import Decimal
    assert Decimal('0.1') + Decimal('0.2') == Decimal('0.3')

    # 列表的扁平化
    groups = [['x1', 'x2'], ['y1', 'y2'], ['z']]
    names = sum(groups, [])
    print('names:', names)


# example 31, *args and **kwargs
def py_base_ex31():
    # as declare
    def _sum(*args):
        print('input args:', args)
        return sum(args)

    print()
    print('*args as declare, and return:', _sum(1, 2, 3))

    # as input
    def _add(a, b):
        return a + b

    tmp_list = [1, 2]
    print('\n*args as input, and return:', _add(*tmp_list))
    tmp_dict = {'a': 1, 'b': 6}
    print('**kwargs as input, and return:', _add(**tmp_dict))

    # list to tuple
    def _print(*val):
        print('\ninput args type:', type(val))
        print('input values:', val)

    vals = ['a', 'b', 'c']
    _print(*vals)


# example 32, check string is int
def py_base_ex32():
    for str in ('11.11', '3.0', '10', '-1', '0'):
        print(str, str.isdigit())


if __name__ == '__main__':

    print('python base demo START.')
    print('PYPATH='+os.getenv('PYPATH')
          if len(os.getenv('PYPATH')) > 0 else 'PYPATH=null')
    print('\npython version:\n', sys.version)
    print()

    py_base_ex32()
    # py_base_ex23_01()

    print('python base demo DONE.')
