# coding: utf-8

import gevent
from gevent import getcurrent
from gevent.pool import Group
from gevent.local import local

group = Group()


def hello(n):
    gevent.sleep(3 - n)
    print('Size of group %s' % len(group))
    print('Hello %d from Greenlet %s' % (n, id(getcurrent())))
    return n


# ex1, Group().map()
def gevent_ex1():
    ''' greenlet 交替执行，但返回结果（list）与输入顺序一致 [0, 1, 2] '''
    res = group.map(hello, range(3))
    print(type(res), res)


# ex2, Group().imap()
def gevent_ex2():
    ''' 返回结果为IMap, 延迟执行 '''
    res = group.imap(hello, range(3))
    print(type(res), list(res))


# ex3, Group().imap_unordered()
def gevent_ex3():
    ''' greenlet 交替执行，先执行完成的先返回结果 [2, 1, 0] '''
    res = group.imap_unordered(hello, range(3))
    print(type(res), list(res))


# ex4, local
class MyLocal(local):

    __slots__ = ('number', 'x')
    initialized = False

    def __init__(self, **kw):
        if self.initialized:
            raise SystemError('__init__ called too many times')
        self.initialized = True
        self.__dict__.update(kw)

    def squared(self):
        return self.number ** 2


def gevent_ex4():
    stash = MyLocal()

    def func1():
        stash.x = 1
        stash.number = 3
        print('x=%d, number=%d' % (stash.x, stash.number))

    def func2():
        stash.y = 2
        print('y=%d' % stash.y)

        try:
            print('x=%d, number=%d' % (stash.x, stash.number))
        except AttributeError:
            print("x is not local to f2")

    g1 = gevent.spawn(func1)
    g2 = gevent.spawn(func2)
    gevent.joinall([g1, g2])


if __name__ == '__main__':

    gevent_ex4()
    print('gevent demo Done.')
