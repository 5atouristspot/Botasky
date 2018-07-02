#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-8-30
Modify on 2018-01-08


@module: boird monitor
@used: monitor of botasky, use to monitor error
"""

import os
import argparse
import requests
import datetime
from time import sleep

from boird.utils.MyLOG import MyLog
from boird.utils.MyFILE import project_abdir, recursiveSearchFile

logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'moosefs.py')
logger = mylog.outputLog()

from boird.utils.MyTHREAD import MyThread

import ConfigParser

config = ConfigParser.ConfigParser()
colConfig = recursiveSearchFile(project_abdir, '*alertConfig.ini')[0]
config.read(colConfig)

# api auth
api_user = config.get('COLLECTION_API', 'user')
api_password = config.get('COLLECTION_API', 'password')

alert_rate = int(config.get('ALERT', 'alert_rate'))

from boird.module.alert import is_on

__all__ = ['post_url', 'MoosefsMaster', 'MoosefsLogger', 'MoosefsCgiserv', 'MoosefsChunk']
__author__ = 'zhihao'

'''
def post_url(arg):
    boird_host, boird_port, api_version, auth_user, auth_pwd, monitor_name, monitor_ip, monitor_port,node_name = arg

    request_info = requests.get(url='http://{boird_host}:{boird_port}/boird/api/{api_version}/moosefs/{node_name}'.format(
        boird_host=boird_host, boird_port=boird_port, api_version=api_version,node_name=node_name),
        auth=(auth_user, auth_pwd),
        params={'monitor_name': monitor_name, 'monitor_ip': monitor_ip, 'monitor_port': monitor_port})
    print request_info
    return request_info
'''


def post_url(boird_host, boird_port, api_version, auth_user, auth_pwd, monitor_name, monitor_ip, monitor_port,
             node_name):
    # boird_host, boird_port, api_version, auth_user, auth_pwd, monitor_name, monitor_ip, monitor_port,node_name = arg

    request_info = requests.get(
        url='http://{boird_host}:{boird_port}/boird/api/{api_version}/moosefs/{node_name}'.format(
            boird_host=boird_host, boird_port=boird_port, api_version=api_version, node_name=node_name),
        auth=(auth_user, auth_pwd),
        params={'monitor_name': monitor_name, 'monitor_ip': monitor_ip, 'monitor_port': monitor_port})
    print request_info
    return request_info


def MoosefsLogger(boird_host, boird_port, api_version, auth_user, auth_pwd, monitor_name):
    '''
    ok_request = retry:quests.get(url='http://192.168.1.116:3621/boird/api/v1000/moosefs/logger',
                              auth=('da', 'xinxin'),
                              params={'monitor_name': 'mfs:mfsmetalogger', 'monitor_ip': '192.168.71.142', 'monitor_port': 0})
    print(ok_request.url)
    '''
    try:
        # justice on_off is on?
        mon_info = is_on(monitor_name)
        if mon_info is not None:
            g_func_list = []
            for i in range(0, len(mon_info)):
                monitor_name, monitor_ip, monitor_port = mon_info[i]
                arg = []
                arg.append(boird_host)
                arg.append(boird_port)
                arg.append(api_version)
                arg.append(auth_user)
                arg.append(auth_pwd)
                arg.append(monitor_name)
                arg.append(monitor_ip)
                arg.append(monitor_port)
                arg.append('logger')
                g_func_list.append({"func": post_url, "args": tuple(arg)})
            mt = MyThread()
            mt.set_thread_func_list(g_func_list)
            mt.start()
    except Exception, e:
        error_msg = "[action]:agent call boird mfsmetalogger api" \
                    "[status]:FAIL" \
                    "[Errorcode]:{e}".format(e=e)
        logger.error(error_msg)


def MoosefsChunk(boird_host, boird_port, api_version, auth_user, auth_pwd, monitor_name):
    '''
    ok_request = retry:quests.get(url='http://192.168.1.116:3621/boird/api/v1000/moosefs/chunk',
                              auth=('da', 'xinxin'),
                              params={'monitor_name': 'mfs:mfschunkserver', 'monitor_ip': '192.168.71.142', 'monitor_port': 0})
    print(ok_request.url)
    '''
    try:
        # justice on_off is on?
        mon_info = is_on(monitor_name)
        if mon_info is not None:
            g_func_list = []
            for i in range(0, len(mon_info)):
                monitor_name, monitor_ip, monitor_port = mon_info[i]
                arg = []
                arg.append(boird_host)
                arg.append(boird_port)
                arg.append(api_version)
                arg.append(auth_user)
                arg.append(auth_pwd)
                arg.append(monitor_name)
                arg.append(monitor_ip)
                arg.append(monitor_port)
                arg.append('chunk')
                g_func_list.append({"func": post_url, "args": tuple(arg)})
            mt = MyThread()
            mt.set_thread_func_list(g_func_list)
            mt.start()

    except Exception, e:
        error_msg = "[action]:agent call boird mfschunkserver api" \
                    "[status]:FAIL" \
                    "[Errorcode]:{e}".format(e=e)
        logger.error(error_msg)


def MoosefsCgiserv(boird_host, boird_port, api_version, auth_user, auth_pwd, monitor_name):
    '''
    ok_request = retry:quests.get(url='http://192.168.1.116:3621/boird/api/v1000/moosefs/cgiserv',
                              auth=('da', 'xinxin'),
                              params={'monitor_name': 'mfs:mfscgiserv', 'monitor_ip': '192.168.71.142', 'monitor_port': 0})
    print(ok_request.url)
    '''
    try:
        # justice on_off is on?
        mon_info = is_on(monitor_name)
        if mon_info is not None:
            g_func_list = []
            for i in range(0, len(mon_info)):
                monitor_name, monitor_ip, monitor_port = mon_info[i]
                arg = []
                arg.append(boird_host)
                arg.append(boird_port)
                arg.append(api_version)
                arg.append(auth_user)
                arg.append(auth_pwd)
                arg.append(monitor_name)
                arg.append(monitor_ip)
                arg.append(monitor_port)
                arg.append('cgiserv')
                g_func_list.append({"func": post_url, "args": tuple(arg)})
            mt = MyThread()
            mt.set_thread_func_list(g_func_list)
            mt.start()
    except Exception, e:
        error_msg = "[action]:agent call boird mfscgiserv api" \
                    "[status]:FAIL" \
                    "[Errorcode]:{e}".format(e=e)
        logger.error(error_msg)


def MoosefsMaster(boird_host, boird_port, api_version, auth_user, auth_pwd, monitor_name):
    '''
    ok_request = retry:quests.get(url='http://192.168.1.116:3621/boird/api/v1000/moosefs/master',
                              auth=('da', 'xinxin'),
                              params={'monitor_name': 'mfs:mfsmaster', 'monitor_ip': '192.168.71.142', 'monitor_port': 0})
    print(ok_request.url)
    '''
    try:
        # justice on_off is on?
        mon_info = is_on(monitor_name)
        if mon_info is not None:
            g_func_list = []
            for i in range(0, len(mon_info)):
                monitor_name, monitor_ip, monitor_port = mon_info[i]
                arg = []
                arg.append(boird_host)
                arg.append(boird_port)
                arg.append(api_version)
                arg.append(auth_user)
                arg.append(auth_pwd)
                arg.append(monitor_name)
                arg.append(monitor_ip)
                arg.append(monitor_port)
                arg.append('master')
                g_func_list.append({"func": post_url, "args": tuple(arg)})

            mt = MyThread()
            mt.set_thread_func_list(g_func_list)
            mt.start()

    except Exception, e:
        error_msg = "[action]:agent call boird mfsmaster api" \
                    "[status]:FAIL" \
                    "[Errorcode]:{e}".format(e=e)
        logger.error(error_msg)


if __name__ == '__main__':
    # MoosefsMaster('1111.111.11.11',222,'v111','auth','pass','mfs:mfsmaster')
    # MoosefsMaster('10.20.4.47',3621,'v1000','da','xinxin','mfs:mfsmaster')
    # MoosefsCgiserv('10.20.4.47',3622,'v1000','da','xinxin','mfs:mfscgiserv')
    MoosefsChunk('10.20.4.47', 3621, 'v1000', 'da', 'xinxin', 'mfs:mfschunkserver')
    # MoosefsLogger('10.20.4.47',3621,'v1000','da','xinxin','mfs:mfsmetalogger')