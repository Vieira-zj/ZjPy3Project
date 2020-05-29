# -*- coding: utf-8 -*-
'''
Created on 2020-05-28
@author: zhengjin
'''

import sys
import os
sys.path.append(os.getenv('PYPATH'))

from pysort import Stack


def reverse_string(input_str: str) -> str:
    '''
    反转字符串
    '''
    start = 0
    end = len(input_str) - 1
    while start < end:
        input_str[start], input_str[end] = input_str[end], input_str[start]
        start += 1
        end -= 1

    return input_str


def is_recycle_string(input_str: str) -> bool:
    '''
    判断回文字符串
    '''
    start = 0
    end = len(input_str) - 1
    while start < end:
        if input_str[start] != input_str[end]:
            return False
        start += 1
        end -= 1
    return True


def test01():
    print('recycle string test:')
    for input_str in ['xyayx', 'ahha', 'haha']:
        print('%s is recycle string: %s' %
              (input_str, str(is_recycle_string(input_str))))


def get_longest_numbers(num_str: str) -> str:
    '''
    找出字符串中最长的连续数字
    '''
    start = tmp_start = 0
    num_len = tmp_len = 0

    for i in range(len(num_str) - 1):
        if num_str[i].isdigit():
            tmp_len += 1
        else:
            tmp_len = 0
            tmp_start = i + 1

        if tmp_len > num_len:
            num_len = tmp_len
            start = tmp_start
    return num_str[start:(start+num_len)]


def test02():
    num_str = 'abcd13579ed124ss123456789z'
    print('longest continuious numbers:', get_longest_numbers(num_str))


def filter_aba_string(aba_str: str) -> str:
    '''
    过滤掉输入字符串中的驼峰字符串（aba）
    input: AaabxbcdyayBxxy
    output: AaacdBxxy
    '''
    def is_aba_string(input_str):
        return input_str[0] == input_str[2]

    local_str = aba_str[:]
    i = 0
    while i < (len(local_str) - 2):
        if is_aba_string(local_str[i:i+3]):
            local_str = local_str[0:i] + local_str[i+3:]
        else:
            i += 1
    return local_str


def test03():
    aba_str = 'AaabxbcdyayBxxy'
    print('src aba string:', aba_str)
    print('filter aba string:', filter_aba_string(aba_str))


# -----------------------------------
# Others
# -----------------------------------

def reverse_by_words(sentence: str) -> str:
    '''
    reverse words divied by space
    input: this is a test
    output: test a is this
    '''
    s = Stack()
    for word in sentence.split(' '):
        s.push(word)

    tmp_list = []
    while s.size() > 0:
        tmp_list.append(s.pop())
    return ' '.join(tmp_list)


def test04():
    sentence = 'this is a test'
    print('src text:', sentence)
    print('text reverse by words:', reverse_by_words(sentence))


if __name__ == '__main__':

    test04()
    print('py alg string demo done.')
