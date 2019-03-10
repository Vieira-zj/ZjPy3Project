# -*- coding: utf-8 -*-
'''
Created on 2019-03-10

@author: zhengjin
'''

import pytest


@pytest.fixture
def fixture_hook_case():
    '''
    run before and after each test case.
    '''
    print('\n[fixture_hook_case] before invoked.')
    yield 0
    print('\n[fixture_hook_case] after invoked.')


@pytest.fixture(scope='module')
def fixture_hook_module():
    '''
    run before and after module.
    '''
    print('\n[fixture_hook_module] before invoked.')
    yield 0
    print('\n[fixture_hook_module] after invoked.')


# @pytest.fixture
@pytest.fixture(scope='session')
def fixture_lang_data():
    '''
    return lang data with session scope.
    '''
    print('\n[fixture_lang_data] init.')
    common_data = {
        'language': ['python', 'java', 'golang', 'javascript', 'c++']
    }
    yield common_data
    # tearup
    print('\n[fixture_lang_data] tearup.')


@pytest.fixture(params=['smtp.gmail.com', 'mail.python.org'])
def fixture_mails_data(request):
    '''
    return each mail item with case scope.
    '''
    mail_addr = request.param
    yield mail_addr
    print('\n[fixture_mails_data] finalizing %s' % mail_addr)
