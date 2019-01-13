# -*- coding: utf-8 -*-
'''
Created on 2019-01-13
@author: zhengjin

Run test demos by using "pytest" module.

pytest commands:
$ py.test -h
$ py.test --version

pytest plugins:
pytest-html
pytest-rerunfailures
'''

import logging
import pytest


class TestPy02(object):

    @pytest.mark.skip(reason='no run')
    def test_01_collections_deque(self):
        names = ['jack', 'leo', 'sam', 'peter', 'jeo']

        import collections
        deque_names = collections.deque(names)
        deque_names.popleft()
        deque_names.appendleft('mark')
        logging.debug(deque_names)

    @pytest.mark.skip(reason='no run')
    def test_02_dict_get_default(self):
        colors = ['red', 'green', 'red', 'blue', 'green', 'red']

        tmp_dict01 = {}
        for color in colors:
            tmp_dict01.setdefault(color, 0)
            tmp_dict01[color] += 1
        logging.debug(tmp_dict01)

        tmp_dict02 = {}
        for color in colors:
            tmp_dict02[color] = tmp_dict02.get(color, 0) + 1
        logging.debug(tmp_dict02)

    def test_03_default_dict(self):
        names = ['jack', 'leo', 'sam', 'peter', 'jeo']

        from collections import defaultdict
        tmp_dict = defaultdict(list)
        for name in names:
            key = len(name)
            tmp_dict[key].append(name)
        logging.debug(tmp_dict)


if __name__ == '__main__':

    pytest.main(['-v', 'py_test02.py'])
