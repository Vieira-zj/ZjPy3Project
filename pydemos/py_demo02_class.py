# -*- coding: utf-8 -*-
'''
Created on 2019-03-17
@author: zhengjin

Python class and meta class examples.
'''

# example 01, 使用函数当做元类
def py_class_ex01():

    def upper_attr(future_class_name, future_class_parents, future_class_attr):
        '''
        Return a class object, attrs are upper case.
        '''
        print('upper_attr is invoked, cls attrs:', future_class_attr.items())
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return type(future_class_name, future_class_parents, uppercase_attr)

    class Foo(metaclass=upper_attr):
        # __metaclass__ = upper_attr
        bar = 'bip'

    print('attr bar:', hasattr(Foo, 'bar'))
    print('attr BAR:', hasattr(Foo, 'BAR'))
    print('BAR:', Foo.BAR)

    f = Foo()
    print('Foo class:', f.__class__)
    print('Foo super class:', f.__class__.__class__)


# example 02, 使用class来当做元类
def py_class_ex02():

    class UpperAttrMetaclass(type):  # extends from type
        def __new__(cls, name, bases, dct):
            print('upper_attr is invoked, cls attrs:', dct.items())
            attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
            uppercase_attr = dict((name.upper(), value) for name, value in attrs)
            return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)

    class Foo(metaclass=UpperAttrMetaclass):
        # __metaclass__ = UpperAttrMetaclass
        bar = 'bip'

    print('attr bar:', hasattr(Foo, 'bar'))
    print('attr BAR:', hasattr(Foo, 'BAR'))
    print('BAR:', Foo.BAR)

    f = Foo()
    print('Foo class:', f.__class__)
    print('Foo super class:', f.__class__.__class__)


# example 03, __new__, __init__, __call__
def py_class_ex03():

    class Foo(object):
        def __new__(cls, *args, **kwargs):
            print('Foo __new__ is invoked, args=%s, kwargs=%s' % (args, kwargs))
            return super(Foo, cls).__new__(cls)

        def __init__(self, value):
            print('Foo __init__ is invoked.')
            self.value = value

        def __call__(cls, *args, **kwargs):
            print('Foo __call__ is invoked, args=%s, kwargs=%s' % (args, kwargs))

    f1 = Foo(1)
    print('f1 value:', f1.value)
    f1('instance1')
    print()
    f2 = Foo(2)
    print('f2 value:', f2.value)
    f2('instance2')


# example 04, __new__, __init__, __call__
def py_class_ex04():

    class Metaclass(type):
        def __new__(cls, name, bases, dct):
            print('Metaclass __new__ is invoked.')
            return super(Metaclass, cls).__new__(cls, name, bases, dct)

        def __call__(self, value):
            print('Metaclass __call__ is invoked.')
            self.val = value  # self == Foo
            return super(Metaclass, self).__call__(self)

    class Foo(metaclass=Metaclass):
        def __init__(self, meta_cls):
            print('Foo __init__ is invoked.')
            print(type(meta_cls))

    f1 = Foo(1)
    print()
    print(f1, [item for item in dir(f1) if not item.startswith('__')])
    # f1_cls = type(f1)
    f1_cls = f1.__class__
    print(f1_cls, [item for item in dir(f1_cls) if not item.startswith('__')])
    f1_super_cls = f1.__class__.__class__
    print(f1_super_cls, [item for item in dir(f1_super_cls) if not item.startswith('__')])

    print('attr val:', hasattr(Foo, 'val'))
    print('attr val:', hasattr(f1, 'val'))
    print('value:', f1.val)


# example 05, __new__方法实现单例
def py_class_ex05():
    
    class Singleton(object):
        def __new__(cls, *args, **kwargs):
            print('Singleton __new__ is invoked.')
            print('args=%s, kwargs=%s' % (args, kwargs))
            if not hasattr(cls, '_instance'):
                cls._instance = super().__new__(cls)
            return cls._instance

        def __init__(self, name):
            print('Singleton __init__ is invoked.')
            print('attr _instance:', hasattr(self, '_instance'))
            self.name = name

    s1 = Singleton('instance01')
    print('s1 name:', s1.name)
    print()
    s2 = Singleton('instance02')
    print('s2 name:', s2.name)
    print()
    print('s1 and s2 are same object:', s1 is s2)


# example 06, 元类实现单例
def py_class_ex06():

    class Singleton(type):
        # invoke __init__ instead of __new__
        def __init__(self, *args, **kwargs):
            print('meta Singleton __init__ is invoked.')
            self._instance = None
            super(Singleton, self).__init__(*args, **kwargs)

        def __call__(self, *args, **kwargs):
            print('meta Singleton __call__ is invoked.')
            if self._instance is None:
                # __call__ => Foo.__init__
                self._instance = super(Singleton, self).__call__(*args, **kwargs)
            return self._instance

    class Foo(metaclass=Singleton):
        def __init__(self):
            print('Foo __init__ is invoked.')

    foo1 = Foo()
    print()
    foo2 = Foo()
    print()
    print(Foo.__dict__)
    print('foo1 and foo2 are same object:', foo1 is foo2)


# example 07, class private and final attributes
def py_class_ex07():

    class Foo(object):
        _cls_private = 'foo_class_private'
        __cls_final = 'foo_class_final'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
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


if __name__ == '__main__':

    py_class_ex07()
    print('python class demo DONE.')
