#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-4-24


@module: MySIGNAL
@used: send signal to moduel
"""

import signal
import functools
import os

from MyLOG import MyLog
from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'MySIGNAL.py')
logger = mylog.outputLog()

__all__ = ['RX_signal', 'TM_signal']
__author__ = 'zhihao'


def RX_signal(signal_type):
    def decorated(func):
        def wrapper(*args, **kwargs):
            def _handle_func(signum, frame):

                try:
                    result = func(*args, **kwargs)
                    exec_info = "[action]:get signal exec function" \
                                "[status]:OK [funtion]:{func_name} " \
                                "[signal type]:{signal_type}".format(func_name=func.__name__, signal_type=signal_type)
                    logger.info(exec_info)
                except Exception, e:
                    print Exception, ":", e
                    result = 'FAIL'
                    error_msg = "[action]:get signal exec function" \
                                "[status]:FAIL [funtion]:{func_name} " \
                                "[signal type]:{signal_type}" \
                                "[Errorcode]:{e}".format(func_name=func.__name__, signal_type=signal_type,
                                                         e=e)
                    logger.error(error_msg)
                return result

            print os.getpid()
            while True:
                signal.signal(signal_type, _handle_func)
                signal.pause()

        return functools.wraps(func)(wrapper)
    return decorated


def TM_signal(pid,signal_type):
    '''
    :param pid: id of process
    :param sig: signum
    :return: function return
    '''
    try:
        os.kill(pid, signal_type)
        exec_info = "[action]:send signal to exec function" \
                    "[status]:OK [pid]:{pid} " \
                    "[signal type]:{signal_type}".format(pid=pid, signal_type=signal_type)
        logger.info(exec_info)

    except Exception, e:
        print Exception, ":", e
        error_msg = "[action]:send signal to exec function" \
                    "[status]:FAIL [pid]:{pid} " \
                    "[signal type]:{signal_type}" \
                    "[Errorcode]:{e}".format(pid=pid, signal_type=signal_type,
                                             e=e)
        logger.info(error_msg)



'''
@RX_signal(signal.SIGALRM)
def aaa():
    print 'aaaaaaaaaaa'


@RX_signal(signal.SIGTERM)
def bbb():
    print 'bbbbbbbbbbbbbbb'
'''

if __name__ == '__main__':

    #bbb()
    #aaa()

    #print dir(signal)

    import MySIGNAL
    help(MySIGNAL)

