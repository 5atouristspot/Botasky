#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-10-23
Modify on 2018-01-09 ,add choice collection info table

@module: alert
@used: alert of boird, use to send message of alert infomation
"""

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import datetime
import time

import requests

from boird.utils.MyLOG import MyLog
from boird.utils.MyFILE import project_abdir, recursiveSearchFile

logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'alert.py')
logger = mylog.outputLog()

from boird.utils.MyCONN import MySQL
from boird.utils.MyMAIL import MyMail
# from boird.utils.MyTHREAD import MyThread_ns
from boird.utils.MyTHREAD import MyThread

import ConfigParser

config = ConfigParser.ConfigParser()
colConfig = recursiveSearchFile(project_abdir, '*alertConfig.ini')[0]
config.read(colConfig)

# alert rate
durning_time0 = int(config.get('DURNING', 'durning_time0'))
durning_time1 = int(config.get('DURNING', 'durning_time1'))
durning_time2 = int(config.get('DURNING', 'durning_time2'))
rate0 = int(config.get('RATE', 'rate0'))
rate1 = int(config.get('RATE', 'rate1'))
rate2 = int(config.get('RATE', 'rate2'))
alert_rate = int(config.get('ALERT', 'alert_rate'))

__all__ = ['get_alert_info_from_DB', 'set_first_error_time', 'get_first_error_time', 'alert_mail', 'alert_message',
           'send_alert', 'is_on']
__author__ = 'zhihao'


def get_alert_info_from_DB(monitor_name, monitor_ip, monitor_port):
    # choice collection_info table
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    if now_month < 10:
        collection_info = 'collection_info_' + str(now_year) + '0' + str(now_month)
    else:
        collection_info = 'collection_info_' + str(now_year) + str(now_month)

    dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                'port': int(config.get('COLLECTION_DB', 'port')),
                'user': config.get('COLLECTION_DB', 'user'),
                'passwd': config.get('COLLECTION_DB', 'pwd'),
                'db': config.get('COLLECTION_DB', 'db'),
                'charset': 'utf8'}

    db = MySQL(dbconfig)

    sql = "select monitor_name,monitor_ip,monitor_port,http_code,exec_code,api_info,create_time from {collection_info} where monitor_name = '{monitor_name}' and " \
          "monitor_ip = '{monitor_ip}' and monitor_port = {monitor_port} order by create_time desc ;". \
        format(collection_info=collection_info, monitor_name=monitor_name, monitor_ip=monitor_ip,
               monitor_port=monitor_port)
    # print sql
    # logger.info(sql)
    db.query(sql)
    result = db.fetchOneRow()
    db.close()

    return result


def set_first_error_time(monitor_name, monitor_ip, monitor_port, first_error_time):
    '''
    set now time or set default time 0.0
    :param monitor_name:
    :param monitor_ip:
    :param monitor_port:
    :param first_error_time:
    :return: 1 --> OK
    :return: False --> error
    '''
    try:
        # if first_error_time == '0.0':
        #    timestrip = first_error_time
        # else:
        #    timestrip = time.mktime(first_error_time.timetuple())
        # timestrip = first_error_time

        dbconfig = {'host': config.get('META', 'host'),
                    'port': int(config.get('META', 'port')),
                    'user': config.get('META', 'user'),
                    'passwd': config.get('META', 'pwd'),
                    'db': config.get('META', 'db'),
                    'charset': 'utf8'}

        db = MySQL(dbconfig)
        sql = "update add_monitor_info set first_error_time='{first_error_time}' " \
              "where monitor_name = '{monitor_name}' and monitor_ip = '{monitor_ip}' " \
              "and monitor_port = {monitor_port} and on_off = 1;".format(monitor_name=monitor_name,
                                                                         monitor_ip=monitor_ip,
                                                                         monitor_port=monitor_port,
                                                                         first_error_time=first_error_time)
        result = db.update(sql)
        db.commit()
        db.close()

        exec_info = "[action]:set first error time" \
                    "[status]:OK" \
                    "[first_error_time]:{first_error_time}" \
                    "[return code]:{result}".format(first_error_time=first_error_time, result=result)
        logger.info(exec_info)

    except Exception, e:
        error_msg = "[action]:iset first error time" \
                    "[status]:FAIL" \
                    "[Errorcode]:{e}" \
                    "[first_error_time]:{first_error_time}".format(first_error_time=first_error_time, e=e)
        logger.error(error_msg)


def get_first_error_time(monitor_name, monitor_ip, monitor_port):
    '''

    :param monitor_name:
    :param monitor_ip:
    :param monitor_port:
    :return:
    '''
    dbconfig = {'host': config.get('META', 'host'),
                'port': int(config.get('META', 'port')),
                'user': config.get('META', 'user'),
                'passwd': config.get('META', 'pwd'),
                'db': config.get('META', 'db'),
                'charset': 'utf8'}

    db = MySQL(dbconfig)

    sql = "select first_error_time from add_monitor_info " \
          "where monitor_name='{monitor_name}' and monitor_ip='{monitor_ip}' " \
          "and monitor_port={monitor_port} and on_off = 1;".format(monitor_name=monitor_name, monitor_ip=monitor_ip,
                                                                   monitor_port=monitor_port)
    db.query(sql)
    result = db.fetchOneRow()
    db.close()

    return result


def alert_mail(subject, content, attachment_list, img_list):
    mail_info = {'mail_host': config.get('MAIL', 'mail_host'),
                 'mail_port': config.get('MAIL', 'mail_port'),
                 'mail_user': config.get('MAIL', 'mail_user'),
                 'mail_pass': config.get('MAIL', 'mail_pass'),
                 'mail_postfix': config.get('MAIL', 'mail_postfix')}

    to_list = config.get('MAIL', 'to_list').split(',')

    mail = MyMail(mail_info)
    # subject = 'test'
    # content = 'test'
    # attachment_list = []
    # img_list = []
    mail.send_mail(to_list, 'plain', subject, content, attachment_list, img_list)


def alert_message(MessageContent):
    '''

    :param MessageContent: content + time ( beacuse cannot send two same message in one day)
    :return:
    '''
    try:
        SpCode = config.get('MESSAGE', 'SpCode')
        LoginName = config.get('MESSAGE', 'LoginName')
        Password = config.get('MESSAGE', 'Password')

        to_list = config.get('MESSAGE', 'to_list')

        request_info = requests.get(
            url='http://sms.api.ums86.com:8899/sms/Api/Send.do',
            params={'SpCode': SpCode, 'LoginName': LoginName, 'Password': Password, 'MessageContent': MessageContent,
                    'UserNumber': to_list, 'SerialNumber': '', 'f': 1, 'ScheduleTime': ''})

        # print request_info.text

        exec_info = "[action]:send alert message" \
                    "[status]:OK" \
                    "[send respond]:{send_respond}".format(send_respond=request_info.text)
        logger.info(exec_info)

    except Exception, e:
        error_msg = "[action]:send alert message" \
                    "[status]:FAIL" \
                    "[Errorcode]:{e}".format(e=e)
        logger.error(error_msg)


def send_message(message, rate):
    g_func_list = []
    for i in range(0, rate):
        message_arr = []
        message_arr.append(message + '-' + str(i))
        g_func_list.append({"func": alert_message, "args": tuple(message_arr)})
    mt = MyThread()
    mt.set_thread_func_list(g_func_list)
    mt.start()


def send_alert(monitor_name, monitor_ip, monitor_port, mail_subject, alert_info):
    try:
        result = get_alert_info_from_DB(monitor_name, monitor_ip, monitor_port)
        http_code = result[3]
        exec_code = result[4]
        create_time = result[6]

        if exec_code == 0 and http_code == 200:
            '''OK info'''
            # first time of get error infomation from DB
            set_first_error_time(monitor_name, monitor_ip, monitor_port, '0.0')

            # time of get error infomation from DB,but first
            error_time = 0

            # error_time - first_error_time
            dur_time = 0

        elif exec_code == 1 and http_code == 200:
            '''error info ,process disappearance'''
            error_time = int(str(time.mktime(create_time.timetuple())).split('.')[0])
            result_time = get_first_error_time(monitor_name, monitor_ip, monitor_port)

            if result_time is not None:
                first_error_time = int(result_time[0].split('.')[0])
                if first_error_time == 0:
                    first_error_time = error_time - 1
                    str_first_error_time = str(first_error_time) + '.0'
                    set_first_error_time(monitor_name, monitor_ip, monitor_port, str_first_error_time)
                    dur_time = error_time - first_error_time
                else:
                    dur_time = error_time - first_error_time

                # make message
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(error_time))
                message_utf8 = alert_info[0] + '-持续时间:' + str(dur_time) + 's-当前时间:' + now_time
                message_uni = message_utf8.decode('utf-8')
                message = message_uni.encode('gbk')
                # message_arr = []

                # send rate
                if 0 < dur_time <= durning_time0:
                    '''
                    #make message
                    for i in range(0, rate0):
                        message_arr.append(message+'-'+str(i))


                    #send mail
                    #alert_mail(mail_subject, message, [], [])

                    #send short message
                    mythns = MyThread_ns()
                    mythns.run(rate0, alert_message, message_arr)
                    '''
                    '''
                    g_func_list = []
                    for i in range(0, rate0):
                        message_arr = []
                        message_arr.append(message + '-' + str(i))
                        g_func_list.append({"func": alert_message, "args": tuple(message_arr)})

                    mt = MyThread()
                    mt.set_thread_func_list(g_func_list)
                    mt.start()
                    '''
                    send_message(message, rate0)

                elif durning_time0 < dur_time <= durning_time1:
                    '''
                    # make message
                    for i in range(0, rate1):
                        message_arr.append(message+'-'+str(i))

                    # send mail
                    #alert_mail(mail_subject, message, [], [])

                    # send short message
                    mythns = MyThread_ns()
                    mythns.run(rate1, alert_message, message_arr)
                    '''
                    '''
                    g_func_list = []
                    for i in range(0, rate1):
                        message_arr = []
                        message_arr.append(message + '-' + str(i))
                        g_func_list.append({"func": alert_message, "args": tuple(message_arr)})

                    mt = MyThread()
                    mt.set_thread_func_list(g_func_list)
                    mt.start()
                    '''
                    send_message(message, rate1)

                elif durning_time1 < dur_time:
                    '''
                    # make message
                    for i in range(0, rate2):
                        message_arr.append(message+'-'+str(i))

                    # send mail
                    #alert_mail(mail_subject, message, [], [])

                    # send short message
                    mythns = MyThread_ns()
                    mythns.run(rate2, alert_message, message_arr)
                    '''
                    '''
                    g_func_list = []
                    for i in range(0, rate2):
                        message_arr = []
                        message_arr.append(message + '-' + str(i))
                        g_func_list.append({"func": alert_message, "args": tuple(message_arr)})

                    mt = MyThread() 
                    mt.set_thread_func_list(g_func_list)
                    mt.start()
                    '''
                    send_message(message, rate2)

        elif exec_code == 2 and http_code == 200:
            '''error info ,Exec Probe cmd Error'''
            error_time = int(str(time.mktime(create_time.timetuple())).split('.')[0])
            result_time = get_first_error_time(monitor_name, monitor_ip, monitor_port)

            if result_time is not None:
                first_error_time = int(result_time[0].split('.')[0])
                if first_error_time == 0:
                    first_error_time = error_time - 1
                    str_first_error_time = str(first_error_time) + '.0'
                    set_first_error_time(monitor_name, monitor_ip, monitor_port, str_first_error_time)
                    dur_time = error_time - first_error_time
                else:
                    dur_time = error_time - first_error_time

                # make message
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(error_time))
                message_utf8 = alert_info[1] + '-持续时间:' + str(dur_time) + 's-当前时间:' + now_time
                message_uni = message_utf8.decode('utf-8')
                message = message_uni.encode('gbk')
                # message_arr = []

                # send rate
                if 0 < dur_time <= durning_time0:
                    '''
                    #make message
                    for i in range(0, rate0):
                        message_arr.append(message+'-'+str(i))

                    #send mail
                    #alert_mail(mail_subject, message, [], [])

                    #send short message
                    mythns = MyThread_ns()
                    mythns.run(rate0, alert_message, message_arr)
                    '''
                    '''
                    g_func_list = []
                    for i in range(0, rate0):
                        message_arr = []
                        message_arr.append(message + '-' + str(i))
                        g_func_list.append({"func": alert_message, "args": tuple(message_arr)})

                    mt = MyThread()
                    mt.set_thread_func_list(g_func_list)
                    mt.start()
                    '''
                    send_message(message, rate0)

                elif durning_time0 < dur_time <= durning_time1:
                    '''
                    # make message
                    for i in range(0, rate1):
                        message_arr.append(message+'-'+str(i))

                    # send mail
                    #alert_mail(mail_subject, message, [], [])

                    # send short message
                    mythns = MyThread_ns()
                    mythns.run(rate1, alert_message, message_arr)
                    '''
                    '''
                    g_func_list = []
                    for i in range(0, rate1):
                        message_arr = []
                        message_arr.append(message + '-' + str(i))
                        g_func_list.append({"func": alert_message, "args": tuple(message_arr)})

                    mt = MyThread()
                    mt.set_thread_func_list(g_func_list)
                    mt.start()
                    '''
                    send_message(message, rate1)


                elif durning_time1 < dur_time:
                    '''
                    # make message
                    for i in range(0, rate2):
                        message_arr.append(message+'-'+str(i))

                    # send mail
                    #alert_mail(mail_subject, message, [], [])

                    # send short message
                    mythns = MyThread_ns()
                    mythns.run(rate2, alert_message, message_arr)
                    '''
                    '''
                    g_func_list = []
                    for i in range(0, rate2):
                        message_arr = []
                        message_arr.append(message + '-' + str(i))
                        g_func_list.append({"func": alert_message, "args": tuple(message_arr)})

                    mt = MyThread()
                    mt.set_thread_func_list(g_func_list)
                    mt.start()
                    '''
                    send_message(message, rate2)

        elif exec_code == 3 and http_code == 200:
            '''error info ,Server machine maybe Down'''
            error_time = int(str(time.mktime(create_time.timetuple())).split('.')[0])
            result_time = get_first_error_time(monitor_name, monitor_ip, monitor_port)

            if result_time is not None:
                first_error_time = int(result_time[0].split('.')[0])
                if first_error_time == 0:
                    first_error_time = error_time - 1
                    str_first_error_time = str(first_error_time) + '.0'
                    set_first_error_time(monitor_name, monitor_ip, monitor_port, str_first_error_time)
                    dur_time = error_time - first_error_time
                else:
                    dur_time = error_time - first_error_time

                # make message
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(error_time))
                message_utf8 = alert_info[2] + '-持续时间:' + str(dur_time) + 's-当前时间:' + now_time
                message_uni = message_utf8.decode('utf-8')
                message = message_uni.encode('gbk')
                # message_arr = []

                # send rate
                if 0 < dur_time <= durning_time0:
                    '''
                    #make message
                    for i in range(0, rate0):
                        message_arr.append(message+'-'+str(i))

                    #send mail
                    #alert_mail(mail_subject, message, [], [])

                    #send short message
                    mythns = MyThread_ns()
                    mythns.run(rate0, alert_message, message_arr)
                    '''
                    '''
                    g_func_list = []
                    for i in range(0, rate0):
                        message_arr = []
                        message_arr.append(message + '-' + str(i))
                        g_func_list.append({"func": alert_message, "args": tuple(message_arr)})

                    mt = MyThread()
                    mt.set_thread_func_list(g_func_list)
                    mt.start()
                    '''
                    send_message(message, rate0)

                elif durning_time0 < dur_time <= durning_time1:
                    '''
                    # make message
                    for i in range(0, rate1):
                        message_arr.append(message+'-'+str(i))

                    # send mail
                    #alert_mail(mail_subject, message, [], [])

                    # send short message
                    mythns = MyThread_ns()
                    mythns.run(rate1, alert_message, message_arr)
                    '''
                    '''
                    g_func_list = []
                    for i in range(0, rate1):
                        message_arr = []
                        message_arr.append(message + '-' + str(i))
                        g_func_list.append({"func": alert_message, "args": tuple(message_arr)})

                    mt = MyThread()
                    mt.set_thread_func_list(g_func_list)
                    mt.start()
                    '''
                    send_message(message, rate1)

                elif durning_time1 < dur_time:

                    '''
                    # make message
                    for i in range(0, rate2):
                        message_arr.append(message+'-'+str(i))

                    # send mail
                    #alert_mail(mail_subject, message, [], [])

                    # send short message
                    mythns = MyThread_ns()
                    mythns.run(rate2, alert_message, message_arr)
                    '''
                    '''
                    g_func_list = []
                    for i in range(0, rate2):
                        message_arr = []
                        message_arr.append(message + '-' + str(i))
                        g_func_list.append({"func": alert_message, "args": tuple(message_arr)})

                    mt = MyThread()
                    mt.set_thread_func_list(g_func_list)
                    mt.start()
                    '''
                    send_message(message, rate2)

        elif http_code != 200:
            '''botasky error info'''
            error_time = int(time.mktime(create_time.timetuple()).split('.')[0])
            message = 'botasky error: http_code is {http_code}'.format(http_code=http_code) \
                      + '__' + str(error_time)

            # send mail
            # alert_mail(mail_subject, message, [], [])

            # send short message
            alert_message(message)
        else:
            '''other error'''
            pass

        exec_info = "[action]:send alert" \
                    "[status]:OK" \
                    "[monitor name]:{monitor_name}" \
                    "[monitor ip]:{monitor_ip}" \
                    "[monitor port]:{monitor_port}".format(monitor_name=monitor_name, monitor_ip=monitor_ip,
                                                           monitor_port=monitor_port)
        logger.info(exec_info)

        # re_exec_info = "'action': 'send alert', 'status': 'OK', 'monitor name': {monitor_name}, " \
        #               "'monitor ip':{monitor_ip}, 'monitor port': {monitor_port}".format(monitor_name=monitor_name, monitor_ip=monitor_ip, monitor_port=monitor_port)

        # return eval(re_exec_info)

    except Exception, e:
        error_msg = "[action]:send alert" \
                    "[status]:FAIL" \
                    "[monitor name]:{monitor_name}" \
                    "[monitor ip]:{monitor_ip}" \
                    "[monitor port]:{monitor_port}" \
                    "[Errorcode]:{e}".format(e=e, monitor_name=monitor_name, monitor_ip=monitor_ip,
                                             monitor_port=monitor_port)

        logger.error(error_msg)
        # re_error_msg = "'action': 'send alert', 'status': 'OK', 'monitor name': {monitor_name}, " \
        #               "'monitor ip':{monitor_ip}, 'monitor port': {monitor_port}, 'Errorcode': {e}".format(e=e, monitor_name=monitor_name, monitor_ip=monitor_ip, monitor_port=monitor_port)

        # return eval(re_error_msg)


# justice monitor on_off is on?
def is_on(monitor_name):
    dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                'port': int(config.get('COLLECTION_DB', 'port')),
                'user': config.get('COLLECTION_DB', 'user'),
                'passwd': config.get('COLLECTION_DB', 'pwd'),
                'db': config.get('COLLECTION_DB', 'db'),
                'charset': 'utf8'}

    db = MySQL(dbconfig)

    sql = "select monitor_name,monitor_ip,monitor_port from add_monitor_info where monitor_name = '{monitor_name}' and " \
          "on_off = 1 ;".format(monitor_name=monitor_name)
    # print sql
    db.query(sql)
    result = db.fetchAllRows()
    db.close()

    return result


if __name__ == '__main__':
    a, b, c = is_on('mfs:mfsmaster')[0]
    print a, b, c

    # print len(is_on('mfs:mfsmaster'))

    # print get_alert_info_from_DB('mfs:mfsmaster','192.168.71.89',0)
    # print get_alert_info_from_DB('mfs:mfsmount', '192.168.71.142',0)
    # print set_first_error_time('mfs:mfscgiserv', '192.168.71.142', 0, datetime.datetime(2017, 10, 19, 14, 55, 52, 401216))
    # print set_first_error_time('mfs:mfscgiserv', '192.168.71.142', 0, '0.0')
    # ss = get_first_error_time('mfs:mfscgiserv', '192.168.71.142', 0)
    # print ss[0].split('.')[0]
    # alert_mail('test', 'test', [], [])
    # alert_message('MySQLxxxxxx')
    # curl -i -X POST "http://sms.api.ums86.com:8899/sms/Api/Send.do?SpCode=236850&LoginName=tjtfkj&Password=b759904dea4f2aba&MessageContent=MySQLceshiduanxin&UserNumber=15002283621&SerialNumber=&f=1&ScheduleTime="
