# -*- coding: utf-8 -*-
'''
Created on 2019-03-31
@author: zhengjin
'''

import asyncio
import functools
import threading
import time


# demo01, start a routine
def py_routinue_demo01(loop):
    async def routinue01():
        print('this is a routinue')

    print('start a routinue')
    coro = routinue01()
    print('run in event loop')
    loop.run_until_complete(coro)


# demo02, return a value from routine
def py_routinue_demo02(loop):
    async def routine02():
        print('this is a routinue')
        return 'pass'

    print('start a routinue')
    coro = routine02()
    print('run in event loop')
    result = loop.run_until_complete(coro)
    print(f'get routinue result: {result}, default None')


# demo03, invoke 2 sub routines
def py_routinue_demo03(loop):
    async def routinue_main():
        print('this is main routine')
        print('wait for sub routine01 complete')
        ret1 = await routinue01()
        print('wait for sub routine02 complete')
        ret2 = await routinue02(ret1)
        return (ret1, ret2)

    async def routinue01():
        print('this is sub routine01')
        await asyncio.sleep(1)
        return 'sub_routine01'

    async def routinue02(arg):
        print('this is sub routine02')
        return f'sub_routine02 get argument: {arg}'

    print('start a routinue')
    coro = routinue_main()
    print('run in event loop')
    result = loop.run_until_complete(coro)
    print(f'get routinue result: {result}')


# demo04, invoke sync func by call_soon
def py_routinue_demo04(loop):
    def callback(args, *, kwargs='default'):
        print(f'function callback, input args: {args}, {kwargs}')
        print('thread =>', threading.current_thread().getName())

    async def routine_main(loop):
        print('register callbacks')
        loop.call_soon(callback, 1)
        wrapped = functools.partial(callback, kwargs='not default')
        loop.call_soon(wrapped, 2)
        await asyncio.sleep(0.5)

    loop.run_until_complete(routine_main(loop))


# demo05, invoke sync func by call_later
def py_routinue_demo05(loop):
    def callback(n):
        print(f'callback {n} invoked')

    async def routine_main(loop):
        print('register callbacks')
        loop.call_later(0.3, callback, 3)
        loop.call_later(0.2, callback, 2)
        loop.call_soon(callback, 0)
        await asyncio.sleep(0.5)

    loop.run_until_complete(routine_main(loop))


# demo06, future
def py_routinue_demo06(loop):
    def foo(future, result):
        print('future status:', future)
        print('set result for future:', result)
        time.sleep(1)
        future.set_result(result)
        print('future status:', future)

    all_done = asyncio.Future()
    loop.call_soon(foo, all_done, 'future_test')
    print('step1: exec in main')
    time.sleep(1)
    print('step2: run in event loop')
    result = loop.run_until_complete(all_done)
    print('return result:', result)
    print('result from future:', all_done.result())


# demo07, await future
def py_routinue_demo07(loop):
    def foo(future, result):
        print('set result for future:', result)
        future.set_result(result)
        print('future status:', future)

    async def routine_main(loop):
        print('create future object')
        all_done = asyncio.Future()
        loop.call_soon(foo, all_done, 'future_await_test')
        result = await all_done
        print('return result:', result)
        print('result from future:', all_done.result())

    loop.run_until_complete(routine_main(loop))


# demo08, future callback
def py_routinue_demo08(loop):
    def callback(future, n):
        print('%s: future done: %s' % (n, future.result()))

    async def register_callbacks(all_done):
        print('register callback to future')
        all_done.add_done_callback(functools.partial(callback, n=1))
        all_done.add_done_callback(functools.partial(callback, n=2))

    async def routine_main(all_done):
        await register_callbacks(all_done)
        print('set result for future')
        all_done.set_result('future_callback_test')
        print('future status:', all_done)

    all_done = asyncio.Future()
    loop.run_until_complete(routine_main(all_done))


# demo09, task
def py_routinue_demo09(loop):
    async def child():
        print('child routine is running')
        return 'child_pass'

    async def routine_main(loop):
        print('wrapped routine to task')
        task = loop.create_task(child())
        # print('cancel task')
        # task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print('task cancel exception!')
        else:
            print('task done, and result:', task.result())

    loop.run_until_complete(routine_main(loop))


# demo10, run multiple routines by wait
def py_routinue_demo10(loop):
    async def num(n):
        print(f'num {n} is running')
        try:
            await asyncio.sleep(n*0.1)
            return n
        except asyncio.CancelledError:
            print(f'num {n} is cancelled')
            raise

    async def routine_main():
        tasks = [num(i) for i in range(10)]
        complete, pending = await asyncio.wait(tasks, timeout=0.5)
        for t in complete:
            print('complete num:', t.result())
        if pending:
            print('cancel non-complete task')
            for t in pending:
                t.cancel()

    loop.run_until_complete(routine_main())


# demo11, run multiple routines by gather
def py_routinue_demo11(loop):
    async def num(n):
        print(f'num {n} is running')
        try:
            await asyncio.sleep(n*0.1)
            return n
        except asyncio.CancelledError:
            print(f'num {n} is cancelled')
            raise

    async def routine_main():
        tasks = [num(i) for i in range(10)]
        complete = await asyncio.gather(*tasks)
        for t in complete:
            print('complete num:', t)

    loop.run_until_complete(routine_main())


# demo12, run multiple routines by as_completed
def py_routinue_demo12(loop):
    async def foo(n):
        print('wait:', n)
        await asyncio.sleep(n)
        return n

    async def routine_main():
        tasks = [asyncio.ensure_future(foo(i)) for i in range(3)]
        for task in asyncio.as_completed(tasks):
            result = await task
            print('task result:', task.result())

    loop.run_until_complete(routine_main())


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    try:
        py_routinue_demo12(loop)
    finally:
        if loop:
            print('close event loop')
            loop.close()
