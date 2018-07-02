#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-8-31
Modify on 2018-01-09 ,add choice collection info table


@module: mfs api
@used: call mfs api
"""

import requests
import datetime
from time import sleep

from boagent.utils.MyTIMEOUT import timeout

from boagent.utils.MyFILE import project_abdir, recursiveSearchFile

from boagent.utils.MyLOG import MyLog
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'mfs.py')
logger = mylog.outputLog()

from boagent.utils.MyCONN import MySQL

import ConfigParser
config = ConfigParser.ConfigParser()
colConfig = recursiveSearchFile(project_abdir, '*colConfig.ini')[0]
config.read(colConfig)

#collection rate
mfsmaster_rate = int(config.get('COLLECTION_RATE', 'mfsmaster'))
mfscgiserv_rate = int(config.get('COLLECTION_RATE', 'mfscgiserv'))
mfschunkserver_rate = int(config.get('COLLECTION_RATE', 'mfschunkserver'))
mfsmetalogger_rate = int(config.get('COLLECTION_RATE', 'mfsmetalogger'))
mfsmount_rate = int(config.get('COLLECTION_RATE', 'mfsmount'))


from boagent.module.choice_collection_info_table import get_table

__all__ = ['MoosefsMaster', 'MoosefsCgiserv', 'MoosefsMount', 'MoosefsChunk', 'MoosefsLogger']
__author__ = 'zhihao'

@timeout(10)
def MoosefsMaster(botasky_host, botasky_port, api_version, auth_user, auth_pwd, mfsmaster_host, mfsmaster_port, muser, mpassword, rate=mfsmaster_rate):
    '''
    ok_request = requests.get(url='http://192.168.1.116:3621/api/v1000/moosefs/master',
                              auth=('da', 'xinxin'),
                              params={'host': '192.168.71.142', 'port': 22, 'muser': 'root',
                                      'mpassword': 'tfkj706tfkj706'})
    print(ok_request.url)
    '''
    #choice collection_info table
    collection_info = get_table()

    try:
        request_info = requests.get(url='http://{botasky_host}:{botasky_port}/api/{api_version}/moosefs/master'.format(botasky_host=botasky_host, botasky_port=botasky_port, api_version=api_version),
                                    auth=(auth_user, auth_pwd),
                                    params={'host': mfsmaster_host, 'port': mfsmaster_port, 'muser': muser, 'mpassword': mpassword})

        text_info = eval(request_info.text)

        #print 'mfsmaster', request_info.status_code, text_info['data'][0], text_info['data'][1], datetime.datetime.now()
        dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                    'port': int(config.get('COLLECTION_DB', 'port')),
                    'user': config.get('COLLECTION_DB', 'user'),
                    'passwd': config.get('COLLECTION_DB', 'pwd'),
                    'db': config.get('COLLECTION_DB', 'db'),
                    'charset': 'utf8'}
        db = MySQL(dbconfig)
        sql = "INSERT INTO {collection_info} (monitor_name, monitor_ip, http_code, exec_code, api_info) " \
              "VALUES ('{v_monitor_name}', '{v_monitor_ip}', {v_http_code}, {v_exec_code}, '{v_api_info}');". \
              format(collection_info=collection_info,v_monitor_name="mfs:mfsmaster", v_http_code=request_info.status_code,
              v_monitor_ip= mfsmaster_host, v_exec_code=text_info['data'][0],
              v_api_info=text_info['data'][1].strip('\n'))
        #print sql
        db.insert(sql)
        db.commit()
        db.close()

        sleep(rate)
    except Exception, e:
        error_msg = "[action]:agent call mfsmaster api" \
                    "[status]:FAIL" \
                        "[Errorcode]:{e}".format(e=e)
        logger.error(error_msg)

        if 'timeout' in error_msg:
            dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                        'port': int(config.get('COLLECTION_DB', 'port')),
                        'user': config.get('COLLECTION_DB', 'user'),
                        'passwd': config.get('COLLECTION_DB', 'pwd'),
                        'db': config.get('COLLECTION_DB', 'db'),
                        'charset': 'utf8'}
            db = MySQL(dbconfig)
            sql = "INSERT INTO {collection_info} (monitor_name, monitor_ip, http_code, exec_code, api_info) " \
                  "VALUES ('{v_monitor_name}', '{v_monitor_ip}', {v_http_code}, {v_exec_code}, '{v_api_info}');".format(
                collection_info=collection_info,v_monitor_name="mfs:mfsmaster", v_http_code=200,
                v_monitor_ip=mfsmaster_host, v_exec_code=3,
                v_api_info='exec MoosefsMaster timeout , server machine maybe down')
            # print sql
            db.insert(sql)
            db.commit()
            db.close()

        sleep(rate)

@timeout(10)
def MoosefsCgiserv(botasky_host, botasky_port, api_version, auth_user, auth_pwd, mfscgiserv_host, mfscgiserv_port, muser, mpassword, rate=mfscgiserv_rate):

    #choice collection_info table
    collection_info = get_table()

    try:
        request_info = requests.get(url='http://{botasky_host}:{botasky_port}/api/{api_version}/moosefs/cgiserv'.format(botasky_host=botasky_host, botasky_port=botasky_port, api_version=api_version),
                                    auth=(auth_user, auth_pwd),
                                    params={'host': mfscgiserv_host, 'port': mfscgiserv_port, 'muser': muser, 'mpassword': mpassword})
        text_info = eval(request_info.text)
        #print 'mfsmaster', request_info.status_code, text_info['data'][0], text_info['data'][1], datetime.datetime.now()
        dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                    'port': int(config.get('COLLECTION_DB', 'port')),
                    'user': config.get('COLLECTION_DB', 'user'),
                    'passwd': config.get('COLLECTION_DB', 'pwd'),
                    'db': config.get('COLLECTION_DB', 'db'),
                    'charset': 'utf8'}
        db = MySQL(dbconfig)
        sql = "INSERT INTO {collection_info} (monitor_name, monitor_ip, http_code, exec_code, api_info) " \
              "VALUES ('{v_monitor_name}', '{v_monitor_ip}', {v_http_code}, {v_exec_code}, '{v_api_info}');".format(collection_info=collection_info,v_monitor_name="mfs:mfscgiserv", v_http_code=request_info.status_code,
                                                                                                                  v_monitor_ip = mfscgiserv_host, v_exec_code=text_info['data'][0],
                                                                                                                  v_api_info = text_info['data'][1].strip('\n'))
        #print sql
        db.insert(sql)
        db.commit()
        db.close()

        sleep(rate)
    except Exception, e:
        error_msg = "[action]:agent call mfscgiserv api" \
                    "[status]:FAIL" \
                    "[Errorcode]:{e}".format(e=e)
        logger.error(error_msg)
        if 'timeout' in error_msg:
            dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                        'port': int(config.get('COLLECTION_DB', 'port')),
                        'user': config.get('COLLECTION_DB', 'user'),
                        'passwd': config.get('COLLECTION_DB', 'pwd'),
                        'db': config.get('COLLECTION_DB', 'db'),
                        'charset': 'utf8'}
            db = MySQL(dbconfig)
            sql = "INSERT INTO {collection_info} (monitor_name, monitor_ip, http_code, exec_code, api_info) " \
                  "VALUES ('{v_monitor_name}', '{v_monitor_ip}', {v_http_code}, {v_exec_code}, '{v_api_info}');".format(
                collection_info=collection_info,v_monitor_name="mfs:mfscgiserv", v_http_code=200,
                v_monitor_ip=mfscgiserv_host, v_exec_code=3,
                v_api_info='exec MoosefsCgiserv timeout , server machine maybe down')
            # print sql
            db.insert(sql)
            db.commit()
            db.close()

        sleep(rate)

@timeout(10)
def MoosefsChunk(botasky_host, botasky_port, api_version, auth_user, auth_pwd, mfschunkserver_host, mfschunkserver_port, muser, mpassword, rate=mfschunkserver_rate):
    #choice collection_info table
    collection_info = get_table()
    try:
        request_info = requests.get(url='http://{botasky_host}:{botasky_port}/api/{api_version}/moosefs/chunk'.format(botasky_host=botasky_host, botasky_port=botasky_port, api_version=api_version),
                                    auth=(auth_user, auth_pwd),
                                    params={'host': mfschunkserver_host, 'port': mfschunkserver_port, 'muser': muser, 'mpassword': mpassword})

        text_info = eval(request_info.text)

        #print 'mfsmaster', request_info.status_code, text_info['data'][0], text_info['data'][1], datetime.datetime.now()
        dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                    'port': int(config.get('COLLECTION_DB', 'port')),
                    'user': config.get('COLLECTION_DB', 'user'),
                    'passwd': config.get('COLLECTION_DB', 'pwd'),
                    'db': config.get('COLLECTION_DB', 'db'),
                    'charset': 'utf8'}
        db = MySQL(dbconfig)
        sql = "INSERT INTO {collection_info} (monitor_name, monitor_ip, http_code, exec_code, api_info) " \
              "VALUES ('{v_monitor_name}', '{v_monitor_ip}', {v_http_code}, {v_exec_code}, '{v_api_info}');".format(collection_info=collection_info,v_monitor_name="mfs:mfschunkserver", v_http_code=request_info.status_code,
                                                                                                                  v_monitor_ip = mfschunkserver_host, v_exec_code=text_info['data'][0],
                                                                                                                  v_api_info = text_info['data'][1].strip('\n'))
        #print sql
        db.insert(sql)
        db.commit()
        db.close()

        sleep(rate)
    except Exception, e:
        error_msg = "[action]:agent call mfschunkserver api" \
                    "[status]:FAIL" \
                    "[Errorcode]:{e}".format(e=e)
        logger.error(error_msg)
        if 'timeout' in error_msg:
            dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                        'port': int(config.get('COLLECTION_DB', 'port')),
                        'user': config.get('COLLECTION_DB', 'user'),
                        'passwd': config.get('COLLECTION_DB', 'pwd'),
                        'db': config.get('COLLECTION_DB', 'db'),
                        'charset': 'utf8'}
            db = MySQL(dbconfig)
            sql = "INSERT INTO {collection_info} (monitor_name, monitor_ip, http_code, exec_code, api_info) " \
                  "VALUES ('{v_monitor_name}', '{v_monitor_ip}', {v_http_code}, {v_exec_code}, '{v_api_info}');".format(
                collection_info=collection_info,v_monitor_name="mfs:mfschunkserver", v_http_code=200,
                v_monitor_ip=mfschunkserver_host, v_exec_code=3,
                v_api_info='exec MoosefsChunk timeout , server machine maybe down')
            # print sql
            db.insert(sql)
            db.commit()
            db.close()

        sleep(rate)


@timeout(10)
def MoosefsLogger(botasky_host, botasky_port, api_version, auth_user, auth_pwd, mfsmetalogger_host, mfsmetalogger_port, muser, mpassword, rate=mfsmetalogger_rate):
    #choice collection_info table
    collection_info = get_table()
    try:
        request_info = requests.get(url='http://{botasky_host}:{botasky_port}/api/{api_version}/moosefs/logger'.format(botasky_host=botasky_host, botasky_port=botasky_port, api_version=api_version),
                                    auth=(auth_user, auth_pwd),
                                    params={'host': mfsmetalogger_host, 'port': mfsmetalogger_port, 'muser': muser, 'mpassword': mpassword})
        text_info = eval(request_info.text)
        #print 'mfsmaster', request_info.status_code, text_info['data'][0], text_info['data'][1], datetime.datetime.now()
        dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                    'port': int(config.get('COLLECTION_DB', 'port')),
                    'user': config.get('COLLECTION_DB', 'user'),
                    'passwd': config.get('COLLECTION_DB', 'pwd'),
                    'db': config.get('COLLECTION_DB', 'db'),
                    'charset': 'utf8'}
        db = MySQL(dbconfig)
        sql = "INSERT INTO {collection_info} (monitor_name, monitor_ip, http_code, exec_code, api_info) " \
              "VALUES ('{v_monitor_name}', '{v_monitor_ip}', {v_http_code}, {v_exec_code}, '{v_api_info}');".format(collection_info=collection_info,v_monitor_name="mfs:mfsmetalogger", v_http_code=request_info.status_code,
                                                                                                                    v_monitor_ip = mfsmetalogger_host, v_exec_code=text_info['data'][0],
                                                                                                                    v_api_info = text_info['data'][1].strip('\n'))
        #print sql
        db.insert(sql)
        db.commit()
        db.close()
        sleep(rate)
    except Exception, e:
        error_msg = "[action]:agent call mfsmetalogger api" \
                    "[status]:FAIL" \
                    "[Errorcode]:{e}".format(e=e)
        logger.error(error_msg)
        if 'timeout' in error_msg:
            dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                        'port': int(config.get('COLLECTION_DB', 'port')),
                        'user': config.get('COLLECTION_DB', 'user'),
                        'passwd': config.get('COLLECTION_DB', 'pwd'),
                        'db': config.get('COLLECTION_DB', 'db'),
                        'charset': 'utf8'}
            db = MySQL(dbconfig)
            sql = "INSERT INTO {collection_info} (monitor_name, monitor_ip, http_code, exec_code, api_info) " \
                  "VALUES ('{v_monitor_name}', '{v_monitor_ip}', {v_http_code}, {v_exec_code}, '{v_api_info}');".format(
                collection_info=collection_info,v_monitor_name="mfs:mfsmetalogger", v_http_code=200,
                v_monitor_ip=mfsmetalogger_host, v_exec_code=3,
                v_api_info='exec MoosefsLogger timeout , server machine maybe down')
            # print sql
            db.insert(sql)
            db.commit()
            db.close()

        sleep(rate)


@timeout(10)
def MoosefsMount(botasky_host, botasky_port, api_version, auth_user, auth_pwd, mfsmount_host, mfsmount_port, muser, mpassword, rate=mfsmount_rate):
    #choice collection_info table
    collection_info = get_table()
    try:
        request_info = requests.get(url='http://{botasky_host}:{botasky_port}/api/{api_version}/moosefs/mount'.format(botasky_host=botasky_host, botasky_port=botasky_port, api_version=api_version),
                                    auth=(auth_user, auth_pwd),
                                    params={'host': mfsmount_host, 'port': mfsmount_port, 'muser': muser, 'mpassword': mpassword})
        text_info = eval(request_info.text)
        #print 'mfsmaster', request_info.status_code, text_info['data'][0], text_info['data'][1], datetime.datetime.now()
        dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                    'port': int(config.get('COLLECTION_DB', 'port')),
                    'user': config.get('COLLECTION_DB', 'user'),
                    'passwd': config.get('COLLECTION_DB', 'pwd'),
                    'db': config.get('COLLECTION_DB', 'db'),
                    'charset': 'utf8'}
        db = MySQL(dbconfig)
        sql = "INSERT INTO {collection_info} (monitor_name, monitor_ip, http_code, exec_code, api_info) " \
              "VALUES ('{v_monitor_name}', '{v_monitor_ip}', {v_http_code}, {v_exec_code}, '{v_api_info}');".format(collection_info=collection_info,v_monitor_name="mfs:mfsmount", v_http_code=request_info.status_code,
                                                                                                                    v_monitor_ip = mfsmount_host, v_exec_code=text_info['data'][0],
                                                                                                                    v_api_info = text_info['data'][1].strip('\n'))
        #print sql
        db.insert(sql)
        db.commit()
        db.close()
        sleep(rate)
    except Exception, e:
        error_msg = "[action]:agent call mfsmount api" \
                    "[status]:FAIL" \
                    "[Errorcode]:{e}".format(e=e)
        logger.error(error_msg)
        if 'timeout' in error_msg:
            dbconfig = {'host': config.get('COLLECTION_DB', 'host'),
                        'port': int(config.get('COLLECTION_DB', 'port')),
                        'user': config.get('COLLECTION_DB', 'user'),
                        'passwd': config.get('COLLECTION_DB', 'pwd'),
                        'db': config.get('COLLECTION_DB', 'db'),
                        'charset': 'utf8'}
            db = MySQL(dbconfig)
            sql = "INSERT INTO {collection_info} (monitor_name, monitor_ip, http_code, exec_code, api_info) " \
                  "VALUES ('{v_monitor_name}', '{v_monitor_ip}', {v_http_code}, {v_exec_code}, '{v_api_info}');".format(
                collection_info=collection_info,v_monitor_name="mfs:mfsmount", v_http_code=200,
                v_monitor_ip=mfsmount_host, v_exec_code=3,
                v_api_info='exec MoosefsMount timeout , server machine maybe down')
            # print sql
            db.insert(sql)
            db.commit()
            db.close()

        sleep(rate)


if __name__ == '__main__':

    print datetime.datetime.now()
    #MoosefsMaster('192.168.71.145', 3621, 'v1000', 'da', 'xinxin', '192.168.71.142', 22, 'root', 'tfkj706tfkj706')
    #MoosefsCgiserv('192.168.1.116', 3621, 'v1000', 'da', 'xinxin', '192.168.71.142', 22, 'root', 'tfkj706tfkj706')
    #MoosefsChunk('192.168.1.116', 3621, 'v1000', 'da', 'xinxin', '192.168.71.143', 22, 'root', 'tfkj706tfkj706')
    #MoosefsLogger('192.168.1.116', 3621, 'v1000', 'da', 'xinxin', '192.168.71.17', 22, 'root', 'tfkj706tfkj706')
    MoosefsLogger('10.20.1.148', 3621, 'v1000', 'da', 'xinxin', '10.20.1.142', 22, 'root', '12345678')
    #MoosefsMount('192.168.1.116', 3621, 'v1000', 'da', 'xinxin', '192.168.71.142', 22, 'root', 'tfkj706tfkj706')
