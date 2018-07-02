#! /usr/bin/python2.7
# -*- coding: utf-8 -*-


"""
Created on 2017-5-12


@module: MyTHREAD
@used: multithreading
"""

from time import sleep


import threading
import threadpool

from MyLOG import MyLog
from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'MyTHREAD.py')
logger = mylog.outputLog()

__all__ = ['MyThread','MyThread_ns']
__author__ = 'zhihao'

#thread safe
class MyThread():
    def __init__(self):
        '''
        used: init args : func_list ,threads
        '''
        self.func_list = None
        self.threads = []

    def set_thread_func_list(self, func_list):
        '''
        :param func_list:
        used: get function
        '''
        self.func_list = func_list


    def start(self):
        '''
        used: start treading
        '''
        #init treading
        for func_dict in self.func_list:
            try:
                if func_dict["args"]:
                    t = threading.Thread(target=func_dict["func"], args=func_dict["args"])
                    t.setDaemon(True)
                    exec_info = "[action]:init mutlithreading task" \
                                "[status]:OK" \
                                "[thread name]:{thread_name}" \
                                "[funtion]:{funtion}" \
                                "[args]:{args}".format(thread_name=t.name, funtion=func_dict["func"],
                                                       args=func_dict["args"])
                    logger.info(exec_info)
                else:
                    t = threading.Thread(target=func_dict["func"])
                    t.setDaemon(True)
                    exec_info = "[action]:init mutlithreading task" \
                                "[status]:OK" \
                                "[thread name]:{thread_name}" \
                                "[funtion]:{funtion}" \
                                "[args]:NULL".format(thread_name=t.name, funtion=func_dict["func"])
                    logger.info(exec_info)

                self.threads.append(t)
            except Exception, e:
                print Exception, ":", e
                error_msg = "[action]:init mutlithreading task" \
                            "[status]:FAIL" \
                            "[funtion]:{funtion}" \
                            "[Errorcode]:{e}".format(funtion=func_dict["func"],e=e)
                logger.error(error_msg)

        for thread_obj in self.threads:
            try:
                thread_obj.start()
                exec_info = "[action]:mutlithreading task distribution" \
                            "[status]:OK" \
                            "[thread name]:{thread_name}" .format(thread_name=thread_obj.name)
                logger.info(exec_info)
            except Exception, e:
                print Exception, ":", e
                error_msg = "[action]:mutlithreading task distribution" \
                            "[status]:FAIL" \
                            "[thread name]:{thread_name}" \
                            "[Errorcode]:{e}".format(thread_name=thread_obj.name,e=e)
                logger.error(error_msg)

        for thread_obj in self.threads:
            try:
                thread_obj.join()
                if thread_obj.isAlive() == False:
                    exec_info = "[action]:mutlithreading task join" \
                                "[status]:OK" \
                                "[thread name]:{thread_name}" .format(thread_name=thread_obj.name)
                    logger.info(exec_info)
            except Exception, e:
                print Exception, ":", e
                error_msg = "[action]:mutlithreading task join" \
                            "[status]:FAIL" \
                            "[thread name]:{thread_name}" \
                            "[Errorcode]:{e}".format(thread_name=thread_obj.name,e=e)
                logger.error(error_msg)
    '''
    def run(func_name, *args):
        # init a mutex
        #mutex = threading.RLock()
        try:
            # have no args
            if len(*args) == 0:

                #mutex.acquire()
                t = threading.Thread(target=func_name)
                t.setDaemon(True)

                t.start()
                try:
                    if t.isAlive() == True:
                        exec_info = "[action]:mutlithreading task distribution" \
                                    "[status]:OK" \
                                    "[thread name]:{thread_name}" \
                                    "[funtion]:{funtion}" \
                                    "[args]:NULL".format(thread_name=t.name,funtion=func_name)
                        logger.info(exec_info)
                except Exception, e:
                    print Exception, ":", e
                    error_msg = "[action]:mutlithreading task distribution" \
                                "[status]:FAIL" \
                                "[thread name]:{thread_name}" \
                                "[funtion]:{funtion}" \
                                "[args]:NULL" \
                                "[Errorcode]:{e}".format(thread_name=t.name,funtion=func_name,e=e)
                    logger.error(error_msg)

                t.join()
                try:
                    if t.isAlive() == False:
                        exec_info = "[action]:mutlithreading task join" \
                                    "[status]:OK" \
                                    "[thread name]:{thread_name}" \
                                    "[funtion]:{funtion}" \
                                    "[args]:NULL".format(thread_name=t.name,funtion=func_name)
                        logger.info(exec_info)
                except Exception, e:
                    print Exception, ":", e
                    error_msg = "[action]:mutlithreading task join" \
                                "[status]:FAIL" \
                                "[thread name]:{thread_name}" \
                                "[funtion]:{funtion}" \
                                "[args]:NULL" \
                                "[Errorcode]:{e}".format(thread_name=t.name,funtion=func_name,e=e)
                    logger.error(error_msg)
                #mutex.release()


            # have args
            else:
                threads = []
                for i in range(len(*args)):
                    # print args[0][i]
                    # get each element of tuple
                    threads.append(threading.Thread(target=func_name, args=args[0][i]))

                for t in threads:
                    t.setDaemon(True)
                    try:
                        t.start()
                        if t.isAlive() == True:
                            exec_info = "[action]:mutlithreading task distribution" \
                                        "[status]:OK" \
                                        "[thread name]:{thread_name}" \
                                        "[funtion]:{funtion}" \
                                        "[args]:{args}".format(thread_name=t.name, funtion=func_name,
                                                               args=args[0][i])
                            logger.info(exec_info)
                    except Exception, e:
                        print Exception, ":", e
                        error_msg = "[action]:mutlithreading task distribution" \
                                    "[status]:FAIL" \
                                    "[thread name]:{thread_name}" \
                                    "[funtion]:{funtion}" \
                                    "[args]:{args}" \
                                    "[Errorcode]:{e}".format(thread_name=t.name, funtion=func_name,
                                                             args=args[0][i],e=e)
                        logger.error(error_msg)

                for t in threads:
                    t.join()
                    try:
                        if t.isAlive() == False:
                            exec_info = "[action]:mutlithreading task join" \
                                        "[status]:OK" \
                                        "[thread name]:{thread_name}" \
                                        "[funtion]:{funtion}" \
                                        "[args]:{args}".format(thread_name=t.name,funtion=func_name,
                                                               args=args[0][i])
                            logger.info(exec_info)
                    except Exception, e:
                        print Exception, ":", e
                        error_msg = "[action]:mutlithreading task join" \
                                    "[status]:FAIL" \
                                    "[thread name]:{thread_name}" \
                                    "[funtion]:{funtion}" \
                                    "[args]:{args}" \
                                    "[Errorcode]:{e}".format(thread_name=t.name,funtion=func_name,
                                                             args=args[0][i],e=e)
                        logger.error(error_msg)

        except Exception, e:
            print Exception, ":", e
            error_msg = "[action]:mutlithreading task" \
                        "[status]:FAIL" \
                        "[Errorcode]:{e}".format(e=e)
            logger.error(error_msg)
        '''


class MyThread_ns():
    '''
    used: not thread safe
    '''
    def __init__(self):
        pass

    @staticmethod
    def run(pitch_num, func_name, *args):
        pool = threadpool.ThreadPool(pitch_num)
        requests = threadpool.makeRequests(func_name, *args)
        [pool.putRequest(req) for req in requests]
        pool.wait()



'''
def aa():
    print 'aaaaaaa'


def bb(x):
    sleep(2)
    print x
    return x


def func1(ret_num):
    sleep(2)
    print "func1 ret:%d" % ret_num
    return ret_num


def func2(ret_num):
    sleep(8)
    print "func2 ret:%d" % ret_num

    return ret_num


def func3():
    sleep(2)
    print "func3 ret:100"
    return 100
'''

if __name__ == '__main__':

    #import MyTHREAD
    #help(MyTHREAD)

    #myth = MyThread()
    #a = [[1,],[2,],[3,],[4,],[5,],[6,],[7,],[8,],[9,],[10,],[11,],[12,],[13,],[14,],[15,],[16,],[17,],[18,]]
    #myth.run(bb,a)
    '''
    #MyThread()
    mt = MyThread()
    g_func_list = []
    g_func_list.append({"func": func1, "args": (1,)})
    g_func_list.append({"func": func2, "args": (2,)})
    g_func_list.append({"func": func3, "args": None})
    mt.set_thread_func_list(g_func_list)
    mt.start()
    '''

    '''
    #MyThread_ns()
    a=['1','2','3','4','5']
    mythns = MyThread_ns()
    mythns.run(2,bb,a)
    '''



