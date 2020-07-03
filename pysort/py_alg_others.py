# -*- coding: utf-8 -*-
'''
Created on 2020-07-03
@author: zhengjin
'''


def alg_demo01(num: int) -> int:
    '''
    某商店规定：3个空汽水瓶可以换1瓶汽水。小张手上有10个空汽水瓶，她最多可以换多少瓶汽水喝？答案是5瓶。
    先用9个空瓶子换3瓶汽水，喝掉3瓶满的，喝完以后4个空瓶子；
    用3个再换1瓶，喝掉这瓶满的，这时候剩2个空瓶子；
    然后你让老板先借给你1瓶汽水，喝掉这瓶满的，喝完以后用3个空瓶子换1瓶满的还给老板。
    如果小张手上有n个空汽水瓶，最多可以换多少瓶汽水喝？
    '''
    if num < 2:
        return 0
    elif num == 2:
        return 1

    ret_num = int(num / 3)
    remained1 = num % 3
    remained2 = ret_num
    ret_num += alg_demo01(remained1 + remained2)
    return ret_num


def alg_test01():
    inputs = (2, 10, 100)
    expected_res = (1, 5, 50)
    for num, expected in zip(inputs, expected_res):
        ret = alg_demo01(num)
        print('%d => %d' % (num, ret))
        assert(ret == expected)


if __name__ == '__main__':

    alg_test01()
    print('py alg demo done.')
