#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-8-30


@module: moosefs mount
@used: monitor the node of moosefs mount (not used now)
"""

from . import api
from flask import request, jsonify

from ..register_verify_user import auth


from boird.utils.MyGO import MyMiko
from boird.utils.MyTIMEOUT import timeout

from boird.utils.MyFILE import project_abdir, recursiveSearchFile
from boird.utils.MyLOG import MyLog
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'mfsmount.py')
logger = mylog.outputLog()


__all__ = ['mfsmount']
__author__ = 'zhihao'


@api.route('/mount', methods=['GET', 'POST'])
@auth.login_required
def mfsmount():
    '''
    monitor mfsmount exist or not,
    if return [0, "1\n"] is right
    if return [0, "0\n"] or hungon is wrong
    if API hungon ,please use time out function to deal it
    '''
    host = request.args.get('host', type=str, default=None)
    port = request.args.get('port', type=int, default=None)
    muser = request.args.get('muser', type=str, default=None)
    mpassword = request.args.get('mpassword', type=str, default=None)

    paramikoconfig = {'username': muser, 'password': mpassword, 'key_file': ''}

    try:
        miko = MyMiko(host, port, paramikoconfig)

        mfsmount_exist_info = miko.exec_cmd(miko.go(), 'df | grep mfsmaster | wc -l')
        exec_info = "[action]:determine whether mfsmount exists or not" \
                    "[status]:OK" \
                    "[host]:{host}" \
                    "[port]:{port}" \
                    "[data]:{mfsmount_exist_info}".format(mfsmount_exist_info=mfsmount_exist_info,
                                                          host=host, port=port)
        logger.info(exec_info)


        return jsonify({'data': mfsmount_exist_info})

    except Exception, e:
        error_msg = "[action]:determine whether mfsmount exists or not" \
                    "[status]:FAIL" \
                    "[host]:{host}" \
                    "[port]:{port}" \
                    "[Errorcode]:{e}".format(e=e, host=host, port=port)

        logger.error(error_msg)

        return jsonify({'data': e})


