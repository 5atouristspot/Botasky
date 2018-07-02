#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-4-24


@module: MyTRACE
@used: traceback of function
"""

import sys, os, linecache

from MyLOG import MyLog
from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'MyTIMEOUT.py')
logger = mylog.outputLog()

__all__ = ['trace']
__author__ = 'zhihao'


def trace(f):
    '''
    :param f: function
    :return:
    '''
    def globaltrace(frame, why, arg):
        if why == "call":
            return localtrace
        return None

    def localtrace(frame, why, arg):
        if why == "line":
            # record the file name and line number of every trace
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            bname = os.path.basename(filename)
            print "{}({}): {}".format(bname, lineno, linecache.getline(filename, lineno).strip('\r\n')),
        return localtrace

    def _f(*args, **kwds):
        sys.settrace(globaltrace)
        result = f(*args, **kwds)
        sys.settrace(None)
        return result
    return _f

'''
@trace
def xxx(x=8):
    print 1
    print 22
    print 333
    return x
'''

if __name__ == '__main__':

    #print xxx(0)

    import MyTRACE
    help(MyTRACE)


