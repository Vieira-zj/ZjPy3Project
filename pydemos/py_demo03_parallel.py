# -*- coding: utf-8 -*-
'''
Created on 2019-03-14
@author: zhengjin

Python multiple process, threads and pool examples.
'''

import os
import time


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


# example 11, 多线程 生产消费模型 condition
products_11 = 5

def py_parallel_demo11():
    import threading

    lock = threading.RLock()
    full_cond = threading.Condition(lock)
    empty_cond = threading.Condition(lock)

    class Producer(threading.Thread):
        def run(self):
            global products_11
            tag = '[Producer (%s:%s)]' % (os.getpid(), self.name)

            while 1:
                if lock.acquire():
                    print(tag, 'get lock')
                    if products_11 < 10:
                        try:
                            time.sleep(1)
                            products_11 += 1
                            print(tag, 'deliver one, now products: %s' % products_11)
                            # empty_cond.notify()  # 不释放锁定
                            empty_cond.notifyAll()
                        finally:
                            if lock:
                                lock.release()
                                time.sleep(0.5)  # 让其他线程有机会获得锁
                    else:
                        print(tag, 'already 10, stop deliver, now products: %s' % products_11)
                        full_cond.wait()  # 自动释放锁定
                        print(tag, 'resume')

    class Consumer(threading.Thread):
        def run(self):
            global products_11
            tag = '[Consumer (%s-%s)]' % (os.getpid(), self.name)

            while 1:
                if lock.acquire():
                    print(tag, 'get lock')
                    if products_11 > 1:
                        try:
                            time.sleep(1)
                            products_11 -= 1
                            print(tag, 'consume one, now products: %s' % products_11)
                            # full_cond.notify()
                            full_cond.notifyAll()
                        finally:
                            if lock:
                                lock.release()
                                time.sleep(0.5)
                    else:
                        print(tag, 'only 1, stop consume, products: %s' % products_11)
                        empty_cond.wait()
                        print(tag, 'resume')

    # main
    for _ in range(1):
        p = Producer()
        p.start()

    for _ in range(3):
        c = Consumer()
        c.start()


# example 12, 多线程 生产消费模型 condition
alist = None

def py_parallel_demo12():
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


# example 13, 多线程 生产消费模型 阻塞队列
def py_parallel_demo13():
    pass


# example 15, 多进程 生产消费模型
def py_parallel_demo15():
    pass


# example 16, 多进程 生产消费模型 阻塞队列
def py_parallel_demo16():
    pass


# example 17, 多线程/多进程池 multiprocessing
def multiple(x):
    import threading
    res = x * 2
    print('[%s:%s] multiple results: %d' %(os.getpid(), threading.current_thread().getName(), res))

def py_parallel_demo17(is_thread=False):
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
        pool.map(multiple, num_list)
    finally:
        if pool:
            pool.close()
            pool.join()


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
        # func "get_page()" must be global
        executor.submit(get_page, url).add_done_callback(parse_page)

    executor.shutdown()
    print('main', os.getpid())


if __name__ == '__main__':

    py_parallel_demo17()
    print('python parallel demo DONE.')
