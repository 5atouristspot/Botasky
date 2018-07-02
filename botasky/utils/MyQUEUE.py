#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-4-07


@module: MyQUEUE
@used: message queue
"""

import multiprocessing
from multiprocessing import Queue

from MyLOG import MyLog
from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'MyQUEUE.py')
logger = mylog.outputLog()

__all__ = ['MyQueue']
__author__ = 'zhihao'


class MyQueue():
    '''
    used: message queue
    '''
    def __init__(self, maxsize, level):
        '''
        uesd : init queue
        :param maxsize: maxsize of queue
        :param level: level of queue (FIFO or LIFO, Priority)
        '''
        self.maxsize = maxsize
        self.level = level

    def build_queue_lock(self):
        '''
        uesd : build queue
        :return : object of queue, lock
        '''
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        if self.level == 'FIFO':
            q = manager.Queue(self.maxsize)
        '''
        elif self.level == 'LIFO':
            q = manager.LifoQueue(self.maxsize)
        elif self.level == 'Priority':
            q = manager.PriorityQueue(self.maxsize)
        '''

        return q, lock


    @staticmethod
    def write(q, lock, message):
        '''
        used: write queue
        :param q: manager queue
        :param lock: queue lock
        :return: returned value
        '''
        lock.acquire()  # get lock
        for value in message:
            try:
                q.put(value, True, 3) #timeout = 3s
                exec_info = "[action]:put into queue until full" \
                            "[status]:OK" \
                            "[full]:NO" \
                            "[queue]:{q}" \
                            "[value]:{value}".format(value=value, q=q)

                logger.info(exec_info)

            except Exception, e:
                error_msg = "[action]:put into queue until full" \
                            "[status]:FAIL" \
                            "[Errorcode]:{e}" \
                            "[full]:YES" \
                            "[queue]:{q}" \
                            "[value]:{value}".format(value=value, q=q, e=e)

                logger.error(error_msg)
                continue



        lock.release()  # release lock


    @staticmethod
    def read(q, get_num):
        '''
        used : read queue
        :param q: manger queue
        :param get_num: number of top queue
        :return: get info of queue
        '''
        res = []
        #get all queue until empty
        if get_num == 0:
            while True:
                if not q.empty():
                    value = q.get(False)
                    print 'Get %s from queue...' % value
                    res.append(value)

                    exec_info = "[action]:get all queue until empty" \
                                "[status]:OK" \
                                "[empty]:NO" \
                                "[queue]:{q}" \
                                "[value]:{value}".format(q=q, value=value)
                    logger.info(exec_info)
                else:
                    exec_info = "[action]:get all queue until empty" \
                                "[status]:OK" \
                                "[empty]:YES" \
                                "[queue]:{q}" \
                                "[value]:{value}".format(q=q, value=value)
                    logger.info(exec_info)
                    break
        # get top num of queue or until empty
        elif get_num > 0:
            for position in range(get_num):
                if not q.empty():
                    value = q.get(False)
                    res.append(value)

                    exec_info = "[action]:get top num of queue or until empty" \
                                "[status]:OK" \
                                "[empty]:NO" \
                                "[queue]:{q}" \
                                "[position]:{position}" \
                                "[value]:{res}".format(position=position, q=q, res=res[position])
                    logger.info(exec_info)
                else:
                    exec_info = "[action]:get top num of queue or until empty" \
                                "[status]:OK" \
                                "[empty]:YES" \
                                "[queue]:{q}" \
                                "[position]:{position}" \
                                "[result]:{res}".format(position=position, q=q, res=res)
                    logger.info(exec_info)
                    break
        else:
            error_msg = "[action]:init number of get queue" \
                        "[status]:FAIL" \
                        "[Errorcode]:number of get queue is mistake!"

            logger.error(error_msg)
            raise Exception('number of get queue is mistake!')

        return res




from MyPROC import MyProc
from time import sleep
'''
myqueue = MyQueue(10, 'FIFO')
myq, myloc = myqueue.build_queue_lock()

@MyQueue.write_queue(myq, myloc)
def f(x):
    for i in range(10):
        print '%s --- %s ' % (i, x)
        sleep(1)
    return "tttttttt"
'''


if __name__ == '__main__':

    #import MyQUEUE
    #help(MyQUEUE)

    '''write'''
    #myqueque = MyQueue(20, 'FIFO')
    #myq,myloc = myqueque.build_queue_lock()
    #message = ['1','2','3','4','5','6','7','8','9','10','11','12']
    #message = ['1', '2', '3', '4', '5', '6']
    MyQueue.write(myq, myloc, message)

    '''read'''
    #res = MyQueue.read(myq, 11)
    #print res

    '''todo:测试与MyPROC 结合使用'''
    #myproc = MyProc()
    #ss = myproc.run(1, MyQueue.read, ((myq, 13),))
    #print ss



