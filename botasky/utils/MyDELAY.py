#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-4-06


@module: MyDELAY
@used: delayed decorator
"""


from threading import Timer

__all__ = ['delayed']
__author__ = 'zhihao'


def delayed(seconds):
    '''
    used : delayed decorator
    :param seconds: delayed time
    :return:
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            t = Timer(seconds, func, args, kwargs)
            t.start()
        return wrapper
    return decorator


if __name__ == '__main__':
    '''
    import datetime

    @delayed(3)
    def xiaorui():
        print datetime.datetime.now()

    #for i in range(10):
    print datetime.datetime.now()
    xiaorui()
    '''
    import MyDELAY
    help(MyDELAY)