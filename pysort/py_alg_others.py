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


def alg_test02():
    input = ['i am a coder', 'Coder Coder', 'Code', 'more coder']
    fc = FindCoder()
    print(fc.find(input))


class FindCoder(object):
    '''
    再给定的字符串数组中，找到包含"Coder"的字符串(不区分大小写)，并将其作为一个新的数组返回。
    结果字符串的顺序按照"Coder"出现的次数递减排列，若两个串中"Coder"出现的次数相同，则保持他们在原数组中的位置关系。

    给定一个字符串数组A和它的大小n, 请返回结果数组。
    保证原数组大小小于等于300, 其中每个串的长度小于等于200. 同时保证一定存在包含coder的字符串。

    输入：["i am a coder","Coder Coder","Code"]
    返回：["Coder Coder","i am a coder"]
    '''

    def find(self, input_list_of_str: list) -> list:
        tmp_list_of_dict = []
        for s in input_list_of_str:
            tmp_list_of_dict.append(self.findWords(s))
        tmp_list_of_dict = [d for d in tmp_list_of_dict if d['length'] > 0]

        ret_list = []
        for d in tmp_list_of_dict:
            self.insertWithOrder(ret_list, d)
        return [item['text'] for item in ret_list]

    def findWords(self, input: str) -> list:
        words = input.split(' ')
        words_list = [word for word in words if word.lower() == 'coder']
        return {'text': input, 'length': len(words_list)}

    def insertWithOrder(self, input_list: list, item_dict: dict):
        for i in range(len(input_list)):
            if input_list[i]['length'] < item_dict['length']:
                input_list.insert(i, item_dict)
                return
            elif input_list[i]['length'] == item_dict['length']:
                if (i+1) < len(input_list):
                    input_list.insert(i+1, item_dict)
                else:
                    input_list.append(item_dict)
                return
        input_list.append(item_dict)


if __name__ == '__main__':

    alg_test02()
    print('py alg demo done.')
