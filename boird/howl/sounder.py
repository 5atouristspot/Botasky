#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-9-30
Modify on 2018-01-08


@module: boird monitor
@used: monitor of botasky, use to monitor error
"""

import os
import argparse

from time import sleep

from boird.utils.MyLOG import MyLog
from boird.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'sounder.py')
logger = mylog.outputLog()

from boird.utils.MyDAEMON import daemonize

from boird.howl.moosefs import MoosefsMaster,MoosefsCgiserv,MoosefsChunk,MoosefsLogger

import ConfigParser
config = ConfigParser.ConfigParser()
colConfig = recursiveSearchFile(project_abdir, '*alertConfig.ini')[0]
config.read(colConfig)

#api auth
api_user = config.get('COLLECTION_API', 'user')
api_password = config.get('COLLECTION_API', 'password')

alert_rate = int(config.get('ALERT', 'alert_rate'))


__all__ = ['main', 'monitor', 'args']
__author__ = 'zhihao'

def args():
    parser = argparse.ArgumentParser(description='botasky agent')

    parser.add_argument('--mfsmaster', action="store_true", default=False, help='determine mfsmaster exists')
    parser.add_argument('--mfscgiserv', action="store_true", default=False, help='determine mfscgiserv exists')
    parser.add_argument('--mfsmount', action="store_true", default=False, help='determine mfsmount exists')
    parser.add_argument('--mfschunkserver', action="store_true", default=False, help='determine mfschunkserver exists')
    parser.add_argument('--mfsmetalogger', action="store_true", default=False, help='determine mfsmetalogger exists')

    parser.add_argument('--keepalive', action="store_true", default=False, help='determine keepalive exists')
    parser.add_argument('--keepalive_vip', action="store_true", default=False, help='determine keepalive vip exists')
    #parser.add_argument('-b', action="store", dest="b")
    #parser.add_argument('-c', action="store", dest="c", type=int)

    parser_info = parser.parse_args()

    return parser_info



def monitor(boird_host, boird_port):
    args_info = args()
    #case when ??
    if args_info.mfsmaster == True:
        while 1:
            sleep(alert_rate)
            MoosefsMaster(boird_host, boird_port, 'v1000', api_user, api_password, 'mfs:mfsmaster')
            #sleep(alert_rate)

    if args_info.mfscgiserv == True:
        while 1:
            sleep(alert_rate)
            MoosefsCgiserv(boird_host, boird_port, 'v1000', api_user, api_password, 'mfs:mfscgiserv')
            #sleep(alert_rate)

    if args_info.mfschunkserver == True:
        while 1:
            print alert_rate
            sleep(alert_rate)
            MoosefsChunk(boird_host, boird_port, 'v1000', api_user, api_password, 'mfs:mfschunkserver')
            #sleep(alert_rate)

    if args_info.mfsmetalogger == True:
        while 1:
            sleep(alert_rate)
            MoosefsLogger(boird_host, boird_port, 'v1000', api_user, api_password, 'mfs:mfsmetalogger')
            #sleep(alert_rate)

    if args_info.mfsmount == True:
        pass

def main():
    #monitor('192.168.1.116', 3621)
    #monitor('0.0.0.0', 0000)
    monitor('10.20.4.47', 3622)

if __name__ == '__main__':
    daemonize('/dev/null', '/tmp/boird_sounder_stdout.log', '/tmp/boird_sounder_stdout.log')
    main()
