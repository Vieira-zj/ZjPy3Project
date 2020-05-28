# -*- coding: utf-8 -*-
'''
Created on 2020-05-28
@author: zhengjin
'''

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


def test01():
    bin_tree = create_bin_tree(range(0, 10))
    print('#1. print bin tree by pre order:')
    pre_order_bin_tree01(bin_tree)
    print('#2. print bin tree by pre order:')
    pre_order_bin_tree02(bin_tree)



def get_tree_max_depth(root_node):
    # TODO:
    pass


if __name__ == '__main__':

    test01()
    print('py alg struct demo done.')
