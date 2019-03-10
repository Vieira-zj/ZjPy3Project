# -*- coding: utf-8 -*-
'''
Created on 2019-03-30

@author: zhengjin
'''

import pytest


@pytest.mark.skip(reason='no run')
class TestPyFixtures01(object):

    def test_fixture_01(self, fixture_lang_data):
        lang = fixture_lang_data['language']
        print('\n[test_fixture_01] languages:', lang)
        assert(len(lang) == 5)

    def test_fixture_02(self, fixture_lang_data):
        lang = fixture_lang_data['language']
        print('\n[test_fixture_02] languages:', lang)
        assert(len(lang) == 5)

    def test_fixture_03(self, fixture_mails_data):
        print('\n[test_fixture_03] mail addr:', fixture_mails_data)
        assert(True)
# TestPyFixtures01 end


@pytest.mark.usefixtures('fixture_hook_case')
@pytest.mark.usefixtures('fixture_hook_module')
class TestPyFixtures02(object):

    def test_fixture_04(self):
        print('[test_fixture_04] is running ...')
        assert(True)
# TestPyFixtures02 end


class TestPyFixtures03(object):

    @pytest.fixture
    def fixture_names_data(self):
        print('\n[fixture_names_data] init names.')
        names = ['henry', 'vieira', 'zhengjin']
        yield names
        print('\n[fixture_names_data] finalizing names.')

    def test_fixture_05(self, fixture_names_data):
        print('\n[test_fixture_05] names:')
        for name in fixture_names_data:
            print(name)
        assert(True)

    def test_fixture_06(self, fixture_names_data):
        print('\n[test_fixture_06] names:', fixture_names_data)
        assert(True)
# TestPyFixtures03 end


if __name__ == '__main__':

    # pytest.main(['-v', '-s', './'])
    pytest.main(['-v', '-s', 'test_pytest_fixtures.py'])
