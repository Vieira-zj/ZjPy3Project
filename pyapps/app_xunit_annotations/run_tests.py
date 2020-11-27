# coding: utf-8
import os
import sys
import importlib
import inspect
from my_tests import MyTestSuite


def run_tests():
    s = MyTestSuite()
    if not hasattr(s, 'tests'):
        print('No tests found!')
        return

    for test in getattr(s, 'tests'):
        print(f"Run test: meta: {test.test_meta}, desc: {test.test_desc}")
        test(s)


def load_and_run_tests(file_name):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(cur_dir, file_name)
    full_name = os.path.splitext(file_name)[0]
    source = importlib.machinery.SourceFileLoader(full_name, file_path)
    imported = source.load_module(full_name)

    test_classes = [value for name, value in vars(imported).items(
    ) if inspect.isclass(value) and hasattr(value, 'tests')]

    if len(test_classes) == 0:
        print('No tests found!')
        return

    for clazz in test_classes:
        _self = clazz()
        for test in getattr(clazz, 'tests'):
            print(f"Run test: meta: {test.test_meta}, desc: {test.test_desc}")
            test(_self)


if __name__ == '__main__':

    # run_tests()
    load_and_run_tests('my_tests.py')
    print('run test demo Done.')
