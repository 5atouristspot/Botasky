#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-8-30


@module: botasky agent
@used: agent of botasky, use to collect infomation
"""

import os
import argparse

from boagent.module.mfs import MoosefsMaster, MoosefsCgiserv, MoosefsChunk, MoosefsLogger, MoosefsMount

from boagent.utils.MyDAEMON import daemonize

from boagent.utils.MyTIMEOUT import TimeoutError

from utils.MyLOG import MyLog
from utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'run.py')
logger = mylog.outputLog()


import ConfigParser
config = ConfigParser.ConfigParser()


__all__ = ['args', 'collection', 'main']
__author__ = 'zhihao'


def args():
    parser = argparse.ArgumentParser(description='botasky agent')

    parser.add_argument('-f', '--defaultfile', help='set configuration files')

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


def collection(botasky_host, botasky_port):
    args_info = args()

    #case when ??

    if args_info.defaultfile:
        config_file = '*' + args_info.defaultfile
        colConfig = recursiveSearchFile(project_abdir, config_file)[0]
        config.read(colConfig)
    else:
        colConfig = recursiveSearchFile(project_abdir, '*colConfig.ini')[0]
        config.read(colConfig)

    # api auth
    api_user = config.get('COLLECTION_API', 'user')
    api_password = config.get('COLLECTION_API', 'password')
    # monited machine
    monit_host = config.get('MONITED_MACHINE', 'host')
    monit_port = int(config.get('MONITED_MACHINE', 'port'))
    monit_user = config.get('MONITED_MACHINE', 'user')
    monit_password = config.get('MONITED_MACHINE', 'password')

    if args_info.mfsmaster == True:
        while 1:
            MoosefsMaster(botasky_host, botasky_port, 'v1000', api_user, api_password, monit_host, monit_port, monit_user, monit_password)


    if args_info.mfscgiserv:
        while 1:
            MoosefsCgiserv(botasky_host, botasky_port, 'v1000', api_user, api_password, monit_host, monit_port, monit_user, monit_password)

    if args_info.mfsmount:
        while 1:
            MoosefsMount(botasky_host, botasky_port, 'v1000', api_user, api_password, monit_host, monit_port, monit_user,monit_password)

    if args_info.mfschunkserver:
        while 1:
            MoosefsChunk(botasky_host, botasky_port, 'v1000', api_user, api_password, monit_host,monit_port, monit_user, monit_password)

    if args_info.mfsmetalogger:
        while 1:
            MoosefsLogger(botasky_host, botasky_port, 'v1000', api_user, api_password, monit_host, monit_port, monit_user, monit_password)

    if args_info.keepalive:
        pass
    if args_info.keepalive_vip:
        pass


def main():
    os.system('figlet boagent')

    daemonize('/dev/null', '/tmp/boagent_stdout.log', '/tmp/boagent_stdout.log')

    #collection('192.168.71.145', 3621)
    #collection('10.20.1.157', 3621)
    collection('10.20.4.47', 3621)



if __name__ == '__main__':
    #collection('192.168.71.145', 3621)
    main()


    """
    CREATE TABLE `collection_info` (
      `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
      `monitor_name` varchar(20) NOT NULL DEFAULT '' COMMENT '监控类型名称',
      `monitor_ip` varchar(20) NOT NULL DEFAULT '' COMMENT '被监控ip',
      `monitor_port` varchar(20) NOT NULL DEFAULT '' COMMENT '被监控port',
      `http_code` int(11) unsigned NOT NULL DEFAULT '0' COMMENT 'http返回码',
      `exec_code` int(11) unsigned NOT NULL DEFAULT '99' COMMENT '执行api返回码 0 成功, 1 命令错误(所监控进程不存在了), 2 执行失败(执行监控命令失败) , 3 所监控的服务器宕机',
      `api_info` varchar(255) NOT NULL DEFAULT '' COMMENT '执行api返回内容',
      `create_time` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '采集时间',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='监控数据采集表';
    """



