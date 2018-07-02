#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-4-21


@module: MyTIMEOUT
@used: execute function time out
"""

import signal
import functools

from MyLOG import MyLog
from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'MyTIMEOUT.py')
logger = mylog.outputLog()

__all__ = ['timeout']
__author__ = 'zhihao'


class TimeoutError(Exception):
    pass

def timeout(seconds):
    def decorated(func):
        def _handle_timeout(signum, frame):
            exec_info = "[action]:exec function timeout " \
                        "[status]:FAIL [funtion]:{func_name} " \
                        "[limit time]:{seconds}s".format(func_name=func.__name__, seconds=seconds)
            raise TimeoutError(exec_info)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return functools.wraps(func)(wrapper)
    return decorated


'''
@timeout(5)
def slowfunc(sleep_time):
    import time
    time.sleep(sleep_time)
'''

if __name__ == '__main__':
    '''
    try:
        slowfunc(6)
    except TimeoutError, e:
        print e
    '''

    #import MyTIMEOUT
    #help(MyTIMEOUT)




