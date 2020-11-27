# coding: utf-8
from typing import List, Callable
from my_annotations import test_meta, test_desc, TestMeta


class MyMetaClass(type):

    def __new__(mcs, classname, bases, class_dict):
        tests: List[Callable] = []
        for item in class_dict.values():
            if callable(item) and hasattr(item, 'test_meta'):
                tests.append(item)
        class_dict['tests'] = tests

        return type.__new__(mcs, classname, bases, class_dict)


class MyTestSuite(metaclass=MyMetaClass):

    @test_desc('test case 01, foo')
    @test_meta(TestMeta(title='case01', priority=1))
    def testCase01(self):
        print('This is test case 01, say foo')

    @test_desc('test case 02, bar')
    @test_meta(TestMeta(title='case02', priority=2))
    def testCase02(self):
        print('This is test case 02, say bar')


if __name__ == '__main__':

    pass
