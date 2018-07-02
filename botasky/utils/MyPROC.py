#! /usr/bin/python2.7
# -*- coding: utf-8 -*-


"""
Created on 2017-3-25


@module: MyPROC
@used: multiprocessing
"""


from multiprocessing import Pool

from MyLOG import MyLog
from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'MyPROC.py')
logger = mylog.outputLog()


__all__ = ['MyProc']
__author__ = 'zhihao'

'''
from time import sleep
def f(x):
    for i in range(10):
        print '%s --- %s ' % (i, x)
        sleep(1)
    return "tttttttt"



def k():
    print "wwwwwwwww"
    sleep(1)
    return "eeeeeeee"
'''


class MyProc():
    """
    used : multiprocessing
    """

    def __init__(self):
        pass

    @staticmethod
    def run(pitch_num, func_name, *args):
        """
        used : multiprocessing
        :param pitch_num : the number of max processing
        :param func_name : function name
        :param *args : function parameter
        """
        try:
            # set the processes max number
            pool = Pool(pitch_num)

            #have no args
            if len(*args) == 0:

                result = pool.apply_async(func_name)

                exec_info = "[action]:mutliprocessing task distribution" \
                            "[status]:OK" \
                            "[funtion]:{funtion}" \
                            "[args]:NULL".format(funtion=func_name)
                logger.info(exec_info)

                pool.close()
                pool.join()

                exec_tasks_status = result.successful()
                # task join
                if exec_tasks_status:
                    exec_info = "[action]:mutliprocessing task join" \
                                "[status]:OK" \
                                "[exec_tasks_status]:{exec_tasks_status}".format(exec_tasks_status=exec_tasks_status)
                    logger.info(exec_info)
                # or not
                else:
                    error_msg = "[action]:mutliprocessing task join" \
                                "[status]:FAIL" \
                                "[exec_tasks_status]:{exec_tasks_status}".format(exec_tasks_status=exec_tasks_status)
                    logger.error(error_msg)

                return result.get()

            #have args
            else:
                result = []
                for i in range(len(*args)):
                    # print args[0][i]
                    # get each element of tuple
                    result.append(pool.apply_async(func_name, args[0][i]))

                    exec_info = "[action]:mutliprocessing task distribution" \
                                "[status]:OK" \
                                "[funtion]:{funtion}" \
                                "[args]:{args}".format(funtion=func_name, args=args[0][i])
                    logger.info(exec_info)

                pool.close()
                pool.join()

                ret_info = []
                for j in range(len(result)):
                    # task join
                    if result[j].successful():
                        exec_info = "[action]:mutliprocessing task join" \
                                    "[status]:OK" \
                                    "[funtion]:{funtion}" \
                                    "[args]:{args}" \
                                    "[tasks_done_status]:{exec_tasks_status}".format(funtion=func_name,
                                                                                     args=args[0][j],
                                                                                     exec_tasks_status=result[j].successful()                                                                                     )
                        logger.info(exec_info)
                        ret_info.append(result[j].get())

                    #or not
                    else:


                        exec_info = "[action]:mutliprocessing task join" \
                                    "[status]:FAIL" \
                                    "[funtion]:{funtion}" \
                                    "[args]:{args}" \
                                    "[tasks_done_status]:{exec_tasks_status}".format(funtion=func_name,
                                                                                     args=args[0][j],
                                                             exec_tasks_status=result[j].successful())
                        logger.error(exec_info)
                        ret_info.append("join FAIL")

                return ret_info

        except Exception, e:
            print Exception, ":", e
            error_msg = "[action]:mutliprocessing task" \
                        "[status]:FAIL" \
                        "[Errorcode]:{e}".format(e=e)
            logger.error(error_msg)


if __name__ == '__main__':

    import MyPROC
    help(MyPROC)

    """
    '''aaa is args tuple of function f'''
    myproc = MyProc()

    aaa = ((1,), (2,), (3,), (4,), (5,))
    ss = myproc.run(16, f, aaa)
    print ss
    """

    """
    aaa = ()
    ss = myproc.run(16, k, aaa)
    print ss
    """
