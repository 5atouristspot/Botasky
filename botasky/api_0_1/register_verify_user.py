#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-7-04
Modify on 2017-12-01

@module: register_verify_user
@used: register and verify user
"""

from users_model import User, Init

from . import api
from flask import request, jsonify

import ConfigParser

from botasky.utils.MyCONN import MySQL

from botasky.utils.MyFILE import project_abdir, recursiveSearchFile

from botasky.utils.MyLOG import MyLog
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'register_verify_user.py')
logger = mylog.outputLog()

__all__ = ['register_user', 'verify_user']
__author__ = 'zhihao'


@api.route('/register', methods=['GET', 'POST'])
def register_user():
    '''API users register'''
    username = request.args.get('username', type=str, default=None)
    password = request.args.get('password', type=str, default=None)

    config = ConfigParser.ConfigParser()
    metaConfig = recursiveSearchFile(project_abdir, '*metaConfig.ini')[0]
    config.read(metaConfig)
    engine = Init.Engine(config.get('META', 'user'), config.get('META', 'pwd'),
                         config.get('META', 'host'), config.get('META', 'port'),
                         config.get('META', 'db'))
    session = Init.Session(engine)
    try:
        Init.Insert_User(session, username, password)
        exec_info = "[action]:register user" \
                    "[status]:OK" \
                    "[username]:{username}".format(username=username)
        logger.info(exec_info)
    except Exception, e:
        error_msg = "[action]:register user" \
                    "[status]:FAIL" \
                    "[username]:{username}" \
                    "[Errorcode]:{e}".format(username=username, e=e)
        logger.error(error_msg)
        return jsonify({'status': '[FAIL]',
                        'msg': 'register fail, may be repeated because of username or password',
                        'data': {'username': username, 'password': password}})

    return jsonify({'status': '[OK]',
                    'msg': 'register OK',
                    'data': {'username': username, 'password': password}})


from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_user(username, password):
    '''API users verify decorator'''
    config = ConfigParser.ConfigParser()
    metaConfig = recursiveSearchFile(project_abdir, '*metaConfig.ini')[0]
    config.read(metaConfig)
    dbconfig = {'host': config.get('META', 'host'),
                'port': int(config.get('META', 'port')),
                'user': config.get('META', 'user'),
                'passwd': config.get('META', 'pwd'),
                'db': config.get('META', 'db'),
                'charset': 'utf8'}

    db = MySQL(dbconfig)
    sql = "select id,name,password_hash from users where name = '{username}'".format(username=username)
    db.query(sql)
    info = db.fetchOneRow()
    db.close()

    check_user = User(id=info[0], name=info[1], password_hash=info[2])

    if not check_user or not check_user.verify_password(password):
        error_msg = "[action]:verify user" \
                    "[status]:FAIL" \
                    "[username]:{username}" \
                    "[verify status]:{status}".format(username=check_user.name,
                                                      status=check_user.verify_password(password))
        logger.error(error_msg)
        return False

    exec_info = "[action]:verify user" \
                "[status]:OK" \
                "[username]:{username}".format(username=username)
    logger.info(exec_info)
    return True

'''
@auth.verify_password
def verify_user(username, password):
    #API users verify decorator
    config = ConfigParser.ConfigParser()
    metaConfig = recursiveSearchFile(project_abdir, '*metaConfig.ini')[0]
    config.read(metaConfig)
    engine = Init.Engine(config.get('META', 'user'), config.get('META', 'pwd'),
                         config.get('META', 'host'), config.get('META', 'port'),
                         config.get('META', 'db'))
    session = Init.Session(engine)
    info = session.execute("select id,name,password_hash from users where name = '{username}'".format(username=username)).first()
    session.close()
    check_user = User(id=info[0], name=info[1], password_hash=info[2])

    if not check_user or not check_user.verify_password(password):
        error_msg = "[action]:verify user" \
                    "[status]:FAIL" \
                    "[username]:{username}" \
                    "[verify status]:{status}".format(username=check_user.name,
                                                      status=check_user.verify_password(password))
        logger.error(error_msg)
        return False

    exec_info = "[action]:verify user" \
                "[status]:OK" \
                "[username]:{username}".format(username=username)
    logger.info(exec_info)
    return True
'''

@api.route('/resource')
@auth.login_required
def get_resource():
    '''verify example'''
    return jsonify({'data': 'Hello'})

"""
@api.route('/verify', methods=['GET', 'POST'])
def verify_user():
    '''API users verify'''
    username = request.args.get('username', type=str, default=None)
    password = request.args.get('password', type=str, default=None)

    engine = Init.Engine('admin', 'tfkj705', '192.168.41.40', 3306, 'zhihao_test')
    session = Init.Session(engine)
    info = session.execute("select * from users where name = '{username}'".format(username=username)).first()
    check_user = User(id=info[0], name=info[1], password_hash=info[2])
    verify_status = check_user.verify_password(password)
    return jsonify({'username': username, 'password': password, 'verify_status': verify_status})
"""
