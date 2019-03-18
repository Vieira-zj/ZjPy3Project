# -*- coding: utf-8 -*-
'''
Created on 2019-03-17
@author: zhengjin

Python class and meta class examples.
'''

# example 01, 使用函数当做元类
def py_class_ex01():

    def upper_attr(*args, **kwargs):
        '''
        Return a class object, attrs are upper case.
        '''
        future_class_name, future_class_parents, future_class_attr = args
        print('upper_attr is invoked, cls attrs:', future_class_attr.items())
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)

        return type(future_class_name, future_class_parents, uppercase_attr)

    class Foo(metaclass=upper_attr):
        # __metaclass__ = upper_attr
        bar = 'bip'

    # main
    print('attr bar:', hasattr(Foo, 'bar'))
    print('attr BAR:', hasattr(Foo, 'BAR'))
    print('BAR:', Foo.BAR)

    f = Foo()
    print('Foo class:', f.__class__)
    print('Foo super class:', f.__class__.__class__)


# example 02, 使用class来当做元类
def py_class_ex02():

    class UpperAttrMetaclass(type):  # extends from "type"
        def __new__(cls, *args, **kwargs):
            name, bases, dct = args
            print('upper_attr is invoked, cls attrs:', dct.items())
            attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
            uppercase_attr = dict((name.upper(), value) for name, value in attrs)

            return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)

    class Foo(metaclass=UpperAttrMetaclass):
        # __metaclass__ = UpperAttrMetaclass
        bar = 'bip'

    # main
    print('attr bar:', hasattr(Foo, 'bar'))
    print('attr BAR:', hasattr(Foo, 'BAR'))
    print('BAR:', Foo.BAR)

    f = Foo()
    print('Foo class:', f.__class__)
    print('Foo super class:', f.__class__.__class__)


# example 03, class: __new__, __init__, __call__
def py_class_ex03():

    class Foo(object):
        # create instance from cls
        def __new__(cls, *args, **kwargs):
            print('Foo __new__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            return super(Foo, cls).__new__(cls)

        # instance self created in __new__ and init
        def __init__(self, *args, **kwargs):
            print('Foo __init__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            self.value = args[0]

        def __call__(cls, *args, **kwargs):
            print('Foo __call__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            # super has no attr __call__
            # return super(Foo, cls).__call__(*args, **kwargs)

    # main
    f1 = Foo(1)
    print('f1 value:', f1.value)
    f1('instance1')
    print()
    f2 = Foo(2)
    print('f2 value:', f2.value)
    f2('instance2')


# example 04, metaclass and class: __new__, __init__, __call__
def py_class_ex04():
    # workflow: 
    # 1) Metaclass.__new__ => Metaclass.__init__ => Metaclass, Foo
    # 2) Metaclass.__call__ => Foo.__new__ => Foo.__init__ => Metaclass.__call__ return => Foo, Foo object

    class Metaclass(type):
        def __new__(cls, *args, **kwargs):
            print('Metaclass __new__ is invoked, args:', args)
            name, bases, dct = args
            return super(Metaclass, cls).__new__(cls, name, bases, dct)

        def __init__(self, *args, **kwargs):
            print('Metaclass __init__ is invoked, args:', args)
            print('Metaclass __init__ self:', self)  # self = Foo

        def __call__(self, *args, **kwargs):
            print('Metaclass __call__ is invoked, args:', args)
            print('Metaclass __call__ self:', self)
            return super(Metaclass, self).__call__(*args, **kwargs)

    class Foo(metaclass=Metaclass):
        def __new__(cls, *args, **kwargs):
            print('Foo __new__ is invoked, args:', args)
            return super(Foo, cls).__new__(cls)

        def __init__(self, *args, **kwargs):
            print('Foo __init__ is invoked, args:', args)
            self.name = args[0]

    # main
    f1 = Foo('1')
    print()

    print(f1, [item for item in dir(f1) if not item.startswith('__')])
    f1_cls = f1.__class__  # f1_cls = type(f1)
    print(f1_cls, [item for item in dir(f1_cls) if not item.startswith('__')])
    f1_super_cls = f1.__class__.__class__
    print(f1_super_cls, [item for item in dir(f1_super_cls) if not item.startswith('__')])
    print()

    print('Foo attr name:', hasattr(Foo, 'name'))
    print('f1 attr name:', hasattr(f1, 'name'))
    print('name:', f1.name)


# example 05, __new__方法实现单例
def py_class_ex05():

    class Singleton(object):
        def __new__(cls, *args, **kwargs):
            print('Singleton __new__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            if not hasattr(cls, '_instance'):
                cls._instance = super(Singleton, cls).__new__(cls)
            return cls._instance

        def __init__(self, *args, **kwargs):
            print('Singleton __init__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            print('self attr _instance:', hasattr(self, '_instance'))
            self.name = args[0]

    # main
    s1 = Singleton('s1')
    print('s1 name:', s1.name)
    print()
    s2 = Singleton('s2')
    print('s2 name:', s2.name)
    print()
    print('s1 and s2 are same object:', s1 is s2)


# example 06, 元类实现单例
def py_class_ex06():

    class Singleton(type):
        def __init__(self, *args, **kwargs):
            print('meta Singleton __init__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            self._instance = None

        def __call__(self, *args, **kwargs):
            print('meta Singleton __call__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            if self._instance is None:
                self._instance = super(Singleton, self).__call__(*args, **kwargs)
            return self._instance

    class Foo(metaclass=Singleton):
        def __init__(self, *args, **kwargs):
            print('Foo __init__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            self.name = args[0]

    # main
    foo1 = Foo('1')
    print('f1 name:', foo1.name)
    print()
    foo2 = Foo('2')
    print('f1 name:', foo2.name)
    print()

    print(Foo.__dict__)
    print('Foo instance:', Foo._instance, foo1, foo2)
    print('foo1 and foo2 are same object:', foo1 is foo2)


# example 07, private and final attrs in class
def py_class_ex07():

    class Foo(object):
        _cls_private = 'foo_class_private'
        __cls_final = 'foo_class_final'

        def __init__(self, *args, **kwargs):
            print('===> foo init')
            self.name = 'foo'
            self._inst_private = 'foo_instance_private'
            self.__inst_final = 'foo_instance_final'

        def get_name(self):
            return self.name

        def get_private_attrs(self):
            return 'cls_private=%s, ins_private=%s' % (self._cls_private, self._inst_private)

        def get_final_attrs(self):
            return 'cls_final=%s, ins_final=%s' % (self.__cls_final, self.__inst_final)

    class Bar(Foo):
        _cls_private = 'bar_class_private'
        __cls_final = 'bar_class_final'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            print('===> bar init')
            self.name = 'bar'
            self._inst_private = 'bar_instance_private'
            self.__inst_final = 'bar_instance_final'

    # main
    f = Foo()
    print('f class private attr:', f._cls_private)
    print('f instance private attr:', f._inst_private)
    print('f class final attr:', f._Foo__cls_final)
    print('f instance final attr:', f._Foo__inst_final)
    print()

    b = Bar()
    print(b.__dict__)
    print('name:', b.get_name())
    print('private attrs:', b.get_private_attrs())
    print('final attrs:', b.get_final_attrs())


# example 08, access global var in class
number = 10

def py_class_ex08():

    # not global access
    # number = 10

    class Foo(object):
        def add_number(self, n):
            global number
            number += n

        def print_number(self):
            global number
            print('number: %d' % number)

    # main
    f = Foo()
    f.print_number()
    f.add_number(1)
    f.print_number()


if __name__ == '__main__':

    py_class_ex08()
    print('python meta class demo DONE.')
