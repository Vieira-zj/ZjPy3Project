# -*- coding: utf-8 -*-
'''
Created on 2019-03-14
@author: zhengjin

Python multiple process, threads and pool examples.
'''

import os
import time


# --------------------------------------------------------------
# Coroutine (协程)
# --------------------------------------------------------------
# example 01, generator
def py_parallel_demo01():

    def generate_numbers(n):
        print('start to generate numbers.')
        for i in range(n):
            print('generate number:', i)
            yield i

    numbers = generate_numbers(5)
    print(dir(numbers))

    print(next(numbers))
    print(next(numbers))
    for number in numbers:
        print(number)


# example 02, coroutine (协程), 生产消费模型
def py_parallel_demo02():
    import threading

    def consumer():
        tag = '[CONSUMER-%s-%s]' % (os.getpid(), threading.currentThread().getName())
        print(tag + ' Start ...')
        ret = ''
        while 1:
            good = yield ret
            if not good:
                return
            print(tag + ' Consuming %s ...' % good)
            time.sleep(1)
            ret = '[%s] 200 OK' % time.strftime(r'%y-%m-%d:%H%M%S')

    def produce(c):
        tag = '[PRODUCER-%s-%s]' % (os.getpid(), threading.currentThread().getName())
        next(c)

        n = 0
        while n < 5:
            n = n + 1
            print(tag + ' Producing %s ...' % n)
            r = c.send(n)
            print(tag + ' Consumer return: %s' % r)
        c.close()

    # main
    c = consumer()
    produce(c)


# --------------------------------------------------------------
# Threads (多线程)
# --------------------------------------------------------------
# example 03, 多线程 生产消费模型 condition (refer example_15)
def py_parallel_demo03():
    import threading

    class Producer(threading.Thread):
        def __init__(self, products, lock, full_cond, empty_cond):
            self.products = products
            self.lock = lock
            self.full_cond = full_cond
            self.empty_cond = empty_cond
            super().__init__()

        def run(self):
            tag = '[Producer (%s:%s)]' % (os.getpid(), self.name)

            while 1:
                if self.lock.acquire():
                    if self.products['value'] < 10:
                        try:
                            self.products['value'] += 1
                            print(tag, 'deliver one, now products: %d' % self.products['value'])
                            self.empty_cond.notify_all()  # 不释放锁
                            time.sleep(1)
                        finally:
                            if self.lock:
                                self.lock.release()
                    else:
                        print(tag, 'already 10, stop deliver, now products: %d' % self.products['value'])
                        self.full_cond.wait()  # 自动释放锁
                        print(tag, 'resume from wait')
                        # 这里没有调用release方法主动释放锁, 使用RLOCK, 可重新获得锁
                time.sleep(0.5)  # 让其他线程有机会获得锁
    # end class

    class Consumer(threading.Thread):
        def __init__(self, products, lock, full_cond, empty_cond):
            self.products = products
            self.lock = lock
            self.full_cond = full_cond
            self.empty_cond = empty_cond
            super().__init__()

        def run(self):
            tag = '[Consumer (%s-%s)]' % (os.getpid(), self.name)
            while 1:
                if self.lock.acquire():
                    if self.products['value'] > 1:
                        try:
                            self.products['value'] -= 1
                            print(tag, 'consume one, now products: %d' % self.products['value'])
                            self.full_cond.notify_all()
                            time.sleep(1)
                        finally:
                            if self.lock:
                                self.lock.release()
                    else:
                        print(tag, 'only 1, stop consume, products: %d' % self.products['value'])
                        self.empty_cond.wait()
                        print(tag, 'resume from wait')
                        # 这里没有调用release方法主动释放锁, 使用RLOCK, 可重新获得锁
                time.sleep(0.5)
    # end class

    # main
    products = {'value': 5}
    lock = threading.RLock()
    full_cond = threading.Condition(lock)
    empty_cond = threading.Condition(lock)

    for _ in range(1):
        p = Producer(products, lock, full_cond, empty_cond)
        p.start()
    for _ in range(3):
        c = Consumer(products, lock, full_cond, empty_cond)
        c.start()


# example 04, 多线程 生产消费模型 condition
alist = None

def py_parallel_demo04():
    import threading

    condition = threading.Condition()

    def doSet():
        global alist
        tag = '[Set (%s:%s)]' % (os.getpid(), threading.currentThread().getName())

        if condition.acquire():
            try:
                print(tag, 'get lock')
                while alist is None:
                    print(tag, 'list is not init, and wait')
                    condition.wait()
                print(tag, 'resume')
                time.sleep(1)
                for i in range(len(alist))[::-1]:
                    alist[i] = 1
                print(tag, 'list updated')
                condition.notify()
            finally:
                if condition:
                    condition.release()

    def doPrint():
        global alist
        tag = '[Print (%s:%s)]' % (os.getpid(), threading.currentThread().getName())

        if condition.acquire():
            try:
                print(tag, 'get lock')
                while alist is None or sum(alist) == 0:
                    print(tag, 'list is not ready, and wait')
                    condition.wait()
                print(tag, 'resume')
                time.sleep(1)
                for i in alist:
                    print(tag, i)
            finally:
                if condition:
                    condition.release()

    def doCreate():
        global alist
        tag = '[Create (%s:%s)]' % (os.getpid(), threading.currentThread().getName())

        if condition.acquire():
            try:
                print(tag, 'get lock')
                if alist is None:
                    time.sleep(1)
                    alist = [0 for _ in range(5)]
                    print(tag, 'list init')
                    condition.notifyAll()
            finally:
                if condition:
                    condition.release()

    # main
    threads = []
    threads.append(threading.Thread(target=doPrint, name='t_print'))
    threads.append(threading.Thread(target=doSet, name='t_set'))
    threads.append(threading.Thread(target=doCreate, name='t_create'))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


# example 05, 多线程 生产消费模型 同步阻塞队列
def py_parallel_demo05():
    import random
    import threading
    from queue import Queue

    q = Queue(maxsize=11)
    for i in range(10):
        q.put(i)
    print('queue init size: %d' % q.qsize())

    class Producer(threading.Thread):
        def run(self):
            tag = 'Producer [%s:%s]' % (os.getpid(), threading.current_thread().getName())
            while 1:
                input_int = random.randint(0, 10)
                print(tag, 'queue size: %d, enqueue value: %d' % (q.qsize(), input_int))
                q.put(input_int, block=True, timeout=10)
                time.sleep(3)

    class Consumer(threading.Thread):
        def run(self):
            tag = 'Consumer [%s:%s]' %(os.getpid(), threading.current_thread().getName())
            while 1:
                output_init = q.get(block=True, timeout=10)
                time.sleep(1)
                print(tag, 'queue size: %d, dequeue value: %d' % (q.qsize(), output_init))

    # main
    for _ in range(1):
        Producer().start()
    for _ in range(2):
        Consumer().start()


# --------------------------------------------------------------
# Process (多进程)
# --------------------------------------------------------------
# example 11, 进程间共享数据 multiprocessing
def py_parallel_demo11():
    import multiprocessing

    def my_update(num, arr):
        print('[%s] my_update is running ...' % os.getpid())
        num.value = 14.1
        for i in range(len(arr)):
            arr[i] = -arr[i]

    num = multiprocessing.Value('d', 1.0)  # decimal
    arr = multiprocessing.Array('i', range(10))  # int
    p = multiprocessing.Process(target=my_update, args=(num, arr))
    p.start()
    p.join()

    print('[%s] main is running ...' % os.getpid())
    print('number:', num.value)
    print('array:', arr[:])


# example 12, 进程间共享数据 manager
def py_parallel_demo12():
    from multiprocessing import Process, Manager

    def my_update(lock, shareValue, shareList, shareDict):
        with lock:
            print('[%s] my_update is running ...' % os.getpid())
            shareValue.value += 1
            for i in range(len(shareList)):
                shareList[i] += 1
            shareDict['key1'] += 1
            shareDict['key2'] += 2
            time.sleep(1)

    manager = Manager()
    shareValue = manager.Value('i', 1)
    shareList = manager.list([1, 2, 3, 4, 5])
    shareDict = manager.dict({'key1': 1, 'key2': 2})

    lock = manager.Lock()
    procs = [Process(target=my_update, args=(lock, shareValue, shareList, shareDict)) for _ in range(10)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print('[%s] main is running ...' % os.getpid())
    print('share value:', shareValue)
    print('share list:', shareList)
    print('share dict:', shareDict)


# example 13, 进程间共享数据 manager
def py_parallel_demo13():
    from multiprocessing import Process, Manager

    class MyProcess(Process):
        def __init__(self, *args, **kwargs):
            locals = kwargs['args']
            self.lock = locals[0]
            self.shareValue = locals[1]
            self.shareList = locals[2]
            self.shareDict = locals[3]
            super().__init__(*args, **kwargs)

        def run(self):
            with self.lock:
                print('[%s] MyProcess is running ...' % self.pid)
                self.shareValue.value += 1
                for i in range(len(self.shareList)):
                    self.shareList[i] += 1
                self.shareDict['key1'] += 1
                self.shareDict['key2'] += 2

                time.sleep(1)
    # end class

    # main
    manager = Manager()
    shareValue = manager.Value('i', 1)
    shareList = manager.list([1, 2, 3, 4, 5])
    shareDict = manager.dict({'key1': 1, 'key2': 2})

    lock = manager.Lock()
    procs = [MyProcess(args=(lock, shareValue, shareList, shareDict)) for _ in range(5)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print('[%s] main is running ...' % os.getpid())
    print('share value:', shareValue)
    print('share list:', shareList)
    print('share dict:', shareDict)


# example 14, 进程间共享数据 manager
def py_parallel_demo14():
    from multiprocessing import Process, Value, Lock
    from multiprocessing.managers import BaseManager

    class Employee(object):
        def __init__(self, name, salary):
            self.name = name
            self.salary = Value('i', salary)

        def increase(self):
            self.salary.value += 100
            time.sleep(1)

        def getPay(self):
            return '%s,%d' % (self.name, self.salary.value)

    class MyManager(BaseManager):
        pass

    def increaseSalary(em, lock):
        with lock:
            print('[%s] increaseSalary is running ...' % os.getpid())
            em.increase()

    # main
    MyManager.register('Employee', Employee)
    manager = MyManager()
    manager.start()
    em = manager.Employee('Henry', 1000)

    lock = Lock()
    procs = [Process(target=increaseSalary, args=(em, lock)) for _ in range(5)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print('[%s] main, Employee pay: %s' % (os.getpid(), em.getPay()))


# example 15, 多进程 生产消费模型
def py_parallel_demo15():
    from multiprocessing import Process, Lock, Condition, Value

    class Producer(Process):
        def __init__(self, products, lock, full_cond, empty_cond):
            self.products = products
            self.lock = lock
            self.full_cond = full_cond
            self.empty_cond = empty_cond
            super().__init__()

        def run(self):
            tag = '[Producer (%s:%s)]' % (self.pid, self.name)
            while 1:
                with self.lock:
                    if self.products.value < 10:
                        self.products.value += 1
                        print(tag, 'deliver one, now products: %d' % self.products.value)
                        self.empty_cond.notify_all()  # 不释放锁定
                        time.sleep(1)
                    else:
                        print(tag, 'already 10, stop deliver, now products: %d' % self.products.value)
                        self.full_cond.wait()  # 自动释放锁定
                        print(tag, 'resume from wait')
                time.sleep(0.5)
    # end class

    class Consumer(Process):
        def __init__(self, products, lock, full_cond, empty_cond):
            self.products = products
            self.lock = lock
            self.full_cond = full_cond
            self.empty_cond = empty_cond
            super().__init__()

        def run(self):
            tag = '[Consumer (%s:%s)]' % (self.pid, self.name)
            while 1:
                with self.lock:
                    if self.products.value > 1:
                        self.products.value -= 1
                        print(tag, 'consume one, now products: %d' % self.products.value)
                        self.full_cond.notify_all()
                        time.sleep(1)
                    else:
                        print(tag, 'only 1, stop consume, products: %d' % self.products.value)
                        self.empty_cond.wait()
                        print(tag, 'resume from wait')
                time.sleep(0.5)
    # end class

    # main
    products = Value('i', 5)
    lock = Lock()
    full_cond = Condition(lock)
    empty_cond = Condition(lock)

    for _ in range(2):
        p = Producer(products, lock, full_cond, empty_cond)
        p.start()
    for _ in range(1):
        c = Consumer(products, lock, full_cond, empty_cond)
        c.start()


# example 16, 多进程 生产消费模型 同步阻塞队列
def py_parallel_demo16():
    import random
    from multiprocessing import Process, Queue

    class Producer(Process):
        def __init__(self, queue):
            self.queue = queue
            super().__init__()

        def run(self):
            tag = '[%s:%s]' % (self.pid, self.name)
            while 1:
                print(tag, 'is running ...')
                input_num = random.randint(0, 10)
                self.queue.put(input_num, block=True, timeout=10)
                print(tag, 'put one number into queue:', input_num)
                time.sleep(1)

    class Consumer(Process):
        def __init__(self, queue):
            self.queue = queue
            super().__init__()

        def run(self):
            tag = '[%s:%s]' % (self.pid, self.name)
            while 1:
                print(tag, 'is running ...')
                output_num = self.queue.get(block=True, timeout=10)
                print(tag, 'get one number from queue:', output_num)
                time.sleep(2)

    # main
    queue = Queue(maxsize=11)
    for i in range(5):
        queue.put(i)

    for _ in range(2):
        Producer(queue).start()
    for _ in range(1):
        Consumer(queue).start()


# example 17, 多进程池 multiprocessing pool
def Foo_17(i):
    print('[%s] Foo is running ...' % os.getpid())
    time.sleep(1)
    return i + 100

def py_parallel_demo17():
    from multiprocessing import Process, Pool

    def Bar_17(arg):
        print('[%s] Bar is callback ...' % os.getpid())
        return arg

    # main
    res_list = []
    pool = Pool(3)
    try:
        for i in range(10):
            res = pool.apply_async(func=Foo_17, args=(i,), callback=Bar_17)
            res_list.append(res)
    finally:
        if pool:
            pool.close()
            pool.join()

    print('[%s] main, results:' % os.getpid())
    for res in res_list:
        print(res.get())


# example 18, 多线程/多进程池 multiprocessing pool map
def multiple(x):
    import threading
    res = x * 2
    print('[%s:%s] %d * 2 = %d' % (os.getpid(), threading.current_thread().getName(), x, res))
    return res

def py_parallel_demo18(is_thread=False):
    from multiprocessing import Pool as ProcessPool
    from multiprocessing.dummy import Pool as ThreadPool

    num_list = []
    for num in range(100):
        num_list.append(num)

    pool = None
    if is_thread:
        pool = ThreadPool(3)
    else:
        pool = ProcessPool(3)

    try:
        ret = pool.map(multiple, num_list)
    finally:
        if pool:
            pool.close()
            pool.join()
    print('results:', ret)


# --------------------------------------------------------------
# Pool Executor (多线程/多进程池)
# --------------------------------------------------------------
# example 21, 多线程/多进程池 concurrent.futures
def get_executor(is_thread=False):
    from concurrent.futures import ThreadPoolExecutor
    from concurrent.futures import ProcessPoolExecutor

    return ThreadPoolExecutor() if is_thread else ProcessPoolExecutor(max_workers=3)

def load_url(url):
    import threading
    import urllib.request as request

    print('[%s:%s] running ...' % (os.getpid(), threading.current_thread().getName()))
    with request.urlopen(url, timeout=5) as conn:
        print('%r page is %d bytes' % (url, len(conn.read())))

def py_parallel_demo21():
    from concurrent.futures import wait, as_completed

    executor = get_executor()
    urls = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
    f_list = []
    for url in urls:
        future = executor.submit(load_url, url)
        f_list.append(future)
    print(wait(f_list, return_when='ALL_COMPLETED'))


# example 22, 多线程/多进程池 concurrent.futures map
def py_parallel_demo22():
    from concurrent.futures import wait, as_completed

    urls = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
    executor = get_executor()
    executor.map(load_url, urls)


# example 23, 多进程池 concurrent.futures callback
def get_page(url):
    import requests
    import threading

    print('<%s:%s> get page [%s]' % (os.getpid(), threading.current_thread().getName(), url))
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError('error get %s, and return code %d' %(url, response.status_code))
    return {'url': url, 'text': response.text}

def py_parallel_demo23():
    import threading

    def parse_page(res):
        res = res.result()
        print('<%s:%s> parse page [%s]' % (os.getpid(), threading.current_thread().getName(), res['url']))
        parse_line = 'url [%s], size: %s\n' % (res['url'], len(res['text']))
        print(parse_line)
        with open(os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/test.out'), 'a') as f:
            f.write(parse_line)

    # main
    executor = get_executor()
    urls = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
    for url in urls:
        # for process, func "get_page()" must be defined global
        executor.submit(get_page, url).add_done_callback(parse_page)

    executor.shutdown()
    print('main', os.getpid())


if __name__ == '__main__':

    py_parallel_demo16()
    print('python parallel demo DONE.')
