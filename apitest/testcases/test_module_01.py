# -*- coding: utf-8 -*-
'''
Created on 2019-03-08

@author: zhengjin
'''

import sys
import pytest

sys.path.append('../../')
from utils import LogManager
from utils import Constants


class TestModule01(object):
    pass
    # TODO:


if __name__ == '__main__':

    pytest.main(['-v', '-s', 'test_module_01.py'])
