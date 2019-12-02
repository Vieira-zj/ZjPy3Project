# -*- coding: utf-8 -*-
'''
Created on 2019-11-08
@author: zhengjin
'''

# -----------------------------------
# Sort
# -----------------------------------


def bubble_sort(iter):
    '''
    冒泡排序（交换排序）O(N*N)
    '''
    size = len(iter)
    for i in range(size - 1):
        is_exchange = False
        for j in range(size - 1 - i):
            if iter[j] > iter[j + 1]:
                iter[j], iter[j + 1] = iter[j+1], iter[j]
                is_exchange = True
        if not is_exchange:
            return


def quick_sort(iter, start, end):
    '''
    快速排序（交换排序）O(N*logN)
    '''
    if start >= end:
        return

    mid = iter[start]
    left = start  # error: left = start + 1
    right = end

    while (left < right):
        while left < right and iter[right] >= mid:
            right -= 1
        while left < right and iter[left] <= mid:
            left += 1
        if left < right:
            iter[left], iter[right] = iter[right], iter[left]

    # 从右开始往左移动 当left=right时 指向比mid小的数
    iter[start] = iter[left]
    iter[left] = mid

    quick_sort(iter, start, left - 1)
    quick_sort(iter, left + 1, end)


def merge_sort(iter):
    '''
    归并排序 O(N*logN)
    '''
    if len(iter) == 1:
        return iter

    mid = int(len(iter) / 2)
    iter1 = merge_sort(iter[:mid])
    iter2 = merge_sort(iter[mid:])
    return merge(iter1, iter2)


def merge(iter1, iter2):
    ret_iter = []
    i = j = 0

    while i < len(iter1) and j < len(iter2):
        if iter1[i] < iter2[j]:
            ret_iter.append(iter1[i])
            i += 1
        else:
            ret_iter.append(iter2[j])
            j += 1

    if i < len(iter1):
        ret_iter.extend(iter1[i:])
    if j < len(iter2):
        ret_iter.extend(iter2[j:])
    return ret_iter


# -----------------------------------
# Search
# -----------------------------------

def bin_search01(val, sort_list, start, end):
    '''
    二分查找 有序数组 O(logN) 递归
    '''
    if start > end:
        return -1

    mid = int(start + (end - start) / 2)
    if val > sort_list[mid]:
        return bin_search01(val, sort_list, mid+1, end)
    elif val < sort_list[mid]:
        return bin_search01(val, sort_list, start, mid-1)
    else:
        return mid


def bin_search02(val, sort_list):
    '''
    二分查找 有序数组 O(logN) 非递归
    '''
    start = 0
    end = len(sort_list) - 1

    while start <= end:
        mid = int(start + (end - start) / 2)
        if val > sort_list[mid]:
            start = mid + 1
        elif val < sort_list[mid]:
            end = mid - 1
        else:
            return mid
    return -1


# -----------------------------------
# Stack
# -----------------------------------

class Stack(object):

    def __init__(self):
        self.top = 0
        self.store_list = []

    def size(self):
        return len(self.store_list)

    def push(self, val):
        self.top += 1
        self.store_list.append(val)

    def pop(self):
        if self.top < 1:
            raise StackEmptyException()
        self.top -= 1
        return self.store_list.pop(self.size() - 1)

    def toString(self):
        if self.size() < 1:
            return '[]'
        return ','.join(self.store_list)


class StackEmptyException(Exception):

    def __init__(self):
        self.value = 'stack is empty'

    def __str__(self):
        # return repr(self.value)
        return self.value


# -----------------------------------
# Tree Iterator
# -----------------------------------

class BinTree(object):

    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None

    def SetLeftNode(self, node):
        self.left = node

    def SetRightNode(self, node):
        self.right = node


def create_bin_tree(int_list):
    nodes = []
    for i in range(0, len(int_list)):
        nodes.append(BinTree(i))

    for i in range(0, int(len(nodes) / 2)):
        nodes[i].SetLeftNode(nodes[i*2 + 1])
        if i*2 + 2 < len(nodes):
            nodes[i].SetRightNode(nodes[i*2 + 2])
    return nodes[0]


def pre_order_bin_tree01(tree_node):
    '''
    按层打印二叉树 从上往下 从左往右（先序遍历-递归）
    '''
    if tree_node is None:
        return
    print(tree_node.value)
    pre_order_bin_tree01(tree_node.left)
    pre_order_bin_tree01(tree_node.right)


def pre_order_bin_tree02(tree_node):
    '''
    按层打印二叉树 从上往下 从左往右（先序遍历-非递归）
    '''
    s = Stack()
    s.push(tree_node)
    try:
        while True:
            node = s.pop()
            print(node.value)
            if node.right != None:
                s.push(node.right)
            if node.left != None:
                s.push(node.left)
    except StackEmptyException as e:
        print(e)


def get_tree_max_depth(root_node):
    # TODO:
    pass


# -----------------------------------
# String
# -----------------------------------


def reverse_string(input_str):
    start = 0
    end = len(input_str) - 1
    while start < end:
        input_str[start], input_str[end] = input_str[end], input_str[start]
        start += 1
        end -= 1

    return input_str


def is_recycle_string(input_str):
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


def get_longest_numbers(num_str):
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
    return num_str[start:start+num_len]


def filter_aba_string(aba_str):
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

# -----------------------------------
# Other
# -----------------------------------


def reverse_by_words(sentence):
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


if __name__ == '__main__':

    # sort
    numbers = [15, 16, 1, 99, 50, 0, 99, 13, 6, 2]
    bubble_sort(numbers)
    print('bubble sort results:', numbers)

    numbers = [15, 16, 1, 7, 99, 50, 0, 99, 13, 7]
    quick_sort(numbers, 0, len(numbers) - 1)
    print('\nquick sort results:', numbers)

    numbers = [3, 16, 14, 8, 99, 53, 0, 99, 8, 32, 66]
    print('\nmerge sort results:', merge_sort(numbers))

    # search
    numbers = [1, 3, 4, 6, 8, 9, 10, 12, 13, 77]
    for val in [1, 12, 77]:
        print('#1. search number %d, and index %d' %
              (val, bin_search01(val, numbers, 0, len(numbers)-1)))
        print('#2. search number %d, and index %d' %
              (val, bin_search02(val, numbers)))

    # tree
    bin_tree = create_bin_tree(range(0, 10))
    print('\n#1. print bin tree by pre order:')
    pre_order_bin_tree01(bin_tree)
    print('#2. print bin tree by pre order:')
    pre_order_bin_tree02(bin_tree)

    # string
    print('\nrecycle string test:')
    for input_str in ['xyayx', 'ahha', 'haha']:
        print('%s is recycle string: %s' %
              (input_str, str(is_recycle_string(input_str))))

    num_str = 'abcd13579ed124ss123456789z'
    print('\nlongest continuious numbers:', get_longest_numbers(num_str))

    aba_str = 'AaabxbcdyayBxxy'
    print('\nsrc aba string:', aba_str)
    print('filter aba string:', filter_aba_string(aba_str))

    # others
    sentence = 'this is a test'
    print('\nsrc text:', sentence)
    print('text reverse by words:', reverse_by_words(sentence))

    print('py sort demo done.')
