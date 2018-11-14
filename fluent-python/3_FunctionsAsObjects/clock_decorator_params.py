#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*_args):
            t0 = time.perf_counter()
            _result = func(*_args)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return result
        return clocked
    return decorate


if __name__=='__main__':

    print('---------------------------------------------------------------------------')
    @clock()
    def snooze1(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze1(.123)
    print('---------------------------------------------------------------------------')
    @clock('{name}: {elapsed}s')
    def snooze2(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze2(.123)
    print('---------------------------------------------------------------------------')
    @clock('{name}({args}) executed in {elapsed:0.3f} seconds')
    def snooze3(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze3(.123)
    print('---------------------------------------------------------------------------')
