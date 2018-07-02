#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-8-29


@module: moosefs logger
@used: monitor the node of moosefs logger
"""

from . import api
from flask import request, jsonify

from ..register_verify_user import auth


from botasky.utils.MyGO import MyMiko

from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
from botasky.utils.MyLOG import MyLog
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'mfsmetalogger.py')
logger = mylog.outputLog()


__all__ = ['mfslogger']
__author__ = 'zhihao'


@api.route('/logger', methods=['GET', 'POST'])
@auth.login_required
def mfslogger():
    '''
    monitor mfsmetalogger exist or not,
    if return [0, "0\n"] is right
    '''
    host = request.args.get('host', type=str, default=None)
    port = request.args.get('port', type=int, default=None)
    muser = request.args.get('muser', type=str, default=None)
    mpassword = request.args.get('mpassword', type=str, default=None)

    paramikoconfig = {'username': muser, 'password': mpassword, 'key_file': ''}
    try:
        miko = MyMiko(host, port, paramikoconfig)
        mfslogger_exist_info = miko.exec_cmd(miko.go(), 'killall -0 mfsmetalogger && echo $?')

        exec_info = "[action]:determine whether mfslogger exists or not" \
                    "[status]:OK" \
                    "[host]:{host}" \
                    "[port]:{port}" \
                    "[data]:{mfslogger_exist_info}".format(mfslogger_exist_info=mfslogger_exist_info,
                                                          host=host, port=port)
        logger.info(exec_info)

        return jsonify({'data': mfslogger_exist_info})

    except Exception, e:
        error_msg = "[action]:determine whether mfslogger exists or not" \
                    "[status]:FAIL" \
                    "[host]:{host}" \
                    "[port]:{port}" \
                    "[Errorcode]:{e}".format(e=e, host=host, port=port)

        logger.error(error_msg)

        return jsonify({'data': e})
