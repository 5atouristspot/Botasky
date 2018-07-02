#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-5-23


@module: MyGEVENT
@used: Coroutine
"""

from time import sleep

import gevent
from gevent import monkey; monkey.patch_all()

from MyLOG import MyLog
from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'MyTHREAD.py')
logger = mylog.outputLog()

__all__ = ['MyGevent']
__author__ = 'zhihao'



class MyGevent():
    def __init__(self):
        '''
        used: init args : func_list ,coroutines
        '''
        self.func_list = None
        self.coroutines = []

    def set_thread_func_list(self, func_list):
        '''
        :param func_list:
        used: get function
        '''
        self.func_list = func_list

    def start(self):
        '''
        used: start Coroutines
        '''
        # init Coroutines
        for func_dict in self.func_list:
            try:
                #have args
                if func_dict["args"]:
                    c = gevent.spawn(func_dict["func"], func_dict["args"])
                    exec_info = "[action]:init Coroutine task" \
                                "[status]:OK" \
                                "[coroutine name]:{coroutine_name}".format(coroutine_name=c)
                    logger.info(exec_info)
                #not have args
                else:
                    c = gevent.spawn(func_dict["func"])
                    exec_info = "[action]:init Coroutine task" \
                                "[status]:OK" \
                                "[coroutine name]:{coroutine_name}".format(coroutine_name=c)
                    logger.info(exec_info)

                self.coroutines.append(c)

            except Exception, e:
                error_msg = "[action]:init Coroutine task" \
                            "[status]:FAIL" \
                            "[funtion]:{funtion}" \
                            "[Errorcode]:{e}".format(funtion=func_dict["func"], e=e)
                logger.error(error_msg)

        #coroutines join
        for coroutine_obj in self.coroutines:
            try:
                coroutine_obj.join()
                exec_info = "[action]:Coroutine task join" \
                            "[status]:OK" \
                            "[coroutine name]:{coroutine_name}".format(coroutine_name=coroutine_obj)
                logger.info(exec_info)

            except Exception, e:
                print Exception, ":", e
                error_msg = "[action]:Coroutine task join" \
                            "[status]:FAIL" \
                            "[coroutine name]:{coroutine_name}" \
                            "[Errorcode]:{e}".format(coroutine_name=coroutine_obj, e=e)
                logger.error(error_msg)


        '''
        try:
            #join Coroutines
            a = gevent.joinall(self.coroutines)
            exec_info = "[action]:Coroutine task join" \
                        "[status]:OK" \
                        "[coroutine name]:{coroutine_name}".format(coroutine_name=a)
            logger.info(exec_info)
        except Exception, e:
            print Exception, ":", e
            error_msg = "[action]:Coroutine task join" \
                        "[status]:FAIL" \
                        "[Errorcode]:{e}".format(e=e)
            logger.error(error_msg)
        '''


'''
import urllib2

def f(url):
    print('GET: %s' % url)
    resp = urllib2.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))
'''

if __name__ == '__main__':

    import MyGEVENT
    help(MyGEVENT)
    '''
    mg = MyGevent()
    g_func_list = []
    g_func_list.append({"func": f, "args": 'https://www.python.org/'})
    g_func_list.append({"func": f, "args": 'https://github.com/'})
    g_func_list.append({"func": f, "args": 'https://www.yahoo.com/'})
    mg.set_thread_func_list(g_func_list)
    mg.start()
    '''

