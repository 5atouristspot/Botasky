#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-8-29


@module: moosefs chunk
@used: monitor the node of moosefs chunk
"""

from . import api
from flask import request, jsonify

from ..register_verify_user import auth


from botasky.utils.MyGO import MyMiko

from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
from botasky.utils.MyLOG import MyLog
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'mfschunkserver.py')
logger = mylog.outputLog()


__all__ = ['chunk']
__author__ = 'zhihao'


@api.route('/chunk', methods=['GET', 'POST'])
@auth.login_required
def chunk():
    '''
    monitor mfschunkserver exist or not,
    if return [0, "0\n"] is right
    '''
    host = request.args.get('host', type=str, default=None)
    port = request.args.get('port', type=int, default=None)
    muser = request.args.get('muser', type=str, default=None)
    mpassword = request.args.get('mpassword', type=str, default=None)

    paramikoconfig = {'username': muser, 'password': mpassword, 'key_file': ''}
    try:
        miko = MyMiko(host, port, paramikoconfig)
        mfschunk_exist_info = miko.exec_cmd(miko.go(), 'killall -0 mfschunkserver && echo $?')

        exec_info = "[action]:determine whether mfschunk exists or not" \
                    "[status]:OK" \
                    "[host]:{host}" \
                    "[port]:{port}" \
                    "[data]:{mfschunk_exist_info}".format(mfschunk_exist_info=mfschunk_exist_info,
                                                          host=host, port=port)
        logger.info(exec_info)

        return jsonify({'data': mfschunk_exist_info})

    except Exception, e:
        error_msg = "[action]:determine whether mfschunk exists or not" \
                    "[status]:FAIL" \
                    "[host]:{host}" \
                    "[port]:{port}" \
                    "[Errorcode]:{e}".format(e=e, host=host, port=port)
        logger.error(error_msg)
        return jsonify({'data': e})
