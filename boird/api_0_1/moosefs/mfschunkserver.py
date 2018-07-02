#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-11-28
Modify on 2018-01-09 , get admin business


@module: moosefs mfschunkserver
@used: monitor the node of moosefs mfschunkserver
"""

from . import api
from flask import request, jsonify


from ..register_verify_user import auth

from boird.utils.MyFILE import project_abdir, recursiveSearchFile
from boird.utils.MyLOG import MyLog
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'mfschunkserver.py')
logger = mylog.outputLog()

from boird.utils.MyCONN import MySQL

from boird.module.alert import send_alert
from boird.module.alert_message_info import message_info

import datetime
import time


import ConfigParser
config = ConfigParser.ConfigParser()
colConfig = recursiveSearchFile(project_abdir, '*alertConfig.ini')[0]
config.read(colConfig)

# business
#business = config.get('BUSINESS', 'busin2')
# admin
#admin = config.get('ADMIN', 'admintor3')


__all__ = ['mfschunkserver']
__author__ = 'zhihao'


@api.route('/chunk', methods=['GET', 'POST'])
@auth.login_required
def mfschunkserver():
    monitor_name = request.args.get('monitor_name', type=str, default=None)
    monitor_ip = request.args.get('monitor_ip', type=str, default=None)
    monitor_port = request.args.get('monitor_port', type=int, default=None)

    # get admin, business
    dbconfig = {'host': config.get('META', 'host'),
                'port': int(config.get('META', 'port')),
                'user': config.get('META', 'user'),
                'passwd': config.get('META', 'pwd'),
                'db': config.get('META', 'db'),
                'charset': 'utf8'}

    db = MySQL(dbconfig)

    sql = "select admin, business from collection_info where monitor_name = '{monitor_name}' and " \
          "monitor_ip = '{monitor_ip}' and monitor_port = {monitor_port};".format(monitor_name=monitor_name, monitor_ip=monitor_ip, monitor_port=monitor_port)
    db.query(sql)
    manager_info = db.fetchOneRow()
    db.close()

    admin, business = manager_info

    mail_subject = 'MFS:mfschunkserver alert'
    alert_info = message_info('MFS:mfschunkserver', admin, business, monitor_ip, monitor_port)

    result = send_alert(monitor_name, monitor_ip, monitor_port, mail_subject, alert_info)

    return jsonify(result)
