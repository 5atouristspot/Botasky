#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-4-05


@module: MyGO
@used: ssh to server
"""


import paramiko

from MyLOG import MyLog
from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'MyGO.py')
logger = mylog.outputLog()

__all__ = ['MyMiko']
__author__ = 'zhihao'


class MyMiko():
    """
    used : go to server ,to execute cmd
    """
    def __init__(self, ip_domain, port, config):
        """
        used : init config and get value
        :param ip_domain : target ip or domain
        :param port : target port
        :param config : paramikoconfig
        """
        try:
            self.ip_domain = ip_domain
            self.port = port

            self.config = config

            init_info = "[action]:MyMiko init" \
                        "[status]:OK" \
                        "[ip_domain]:{ip_domain}" \
                        "[port]:{port}" \
                        "[config]:{config}".format(ip_domain=self.ip_domain, port=self.port, config=self.config)
            logger.info(init_info)

        except Exception, e:
            print Exception, ":", e
            error_msg = "[action]:MyMiko init" \
                        "[status]:FAIL" \
                        "[Errorcode]:{e}" \
                        "[ip_domain]:{ip_domain}" \
                        "[port]:{port}" \
                        "[config]:{config}".format(ip_domain=self.ip_domain, port=self.port, config=self.config,
                                                   e=e)
            logger.error(error_msg)

    def go(self):
        """
        used : go to server
        """

        username = self.config['username']
        password = self.config['password']
        key_file = self.config['key_file']
        paramiko_log = recursiveSearchFile(project_abdir, '*paramiko.log')[0]
        paramiko.util.log_to_file(paramiko_log)
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #go to server
        try:
            if key_file == '' and (username != '' and password != ''):

                s.connect(self.ip_domain, self.port, username, password)

            elif key_file != '':

                key = paramiko.RSAKey.from_private_key_file(key_file)
                s.connect(self.ip_domain, self.port, username, pkey=key)

            else:
                error_msg = "[action]:get paramikoconfig " \
                            "[status]:FAIL" \
                            "[Errorcode]:paramikoconfig error" \
                            "[ip_domain]:{ip_domain}" \
                            "[port]:{port}" \
                            "[username]:{username}" \
                            "[password]:{password}" \
                            "[key_file]:{key_file}".format(ip_domain=self.ip_domain, port=self.port,
                                                 username=username, password=password, key_file=key_file)
                logger.error(error_msg)
                return 'paramikoconfig error'

            exec_info = "[action]:go to server" \
                        "[status]:OK" \
                        "[ip_domain]:{ip_domain}" \
                        "[port]:{port}".format(ip_domain=self.ip_domain, port=self.port)
            logger.info(exec_info)
            return s

        except Exception, e:
            error_msg = "[action]:go to server" \
                        "[status]:FAIL" \
                        "[Errorcode]:{e}" \
                        "[ip_domain]:{ip_domain}" \
                        "[port]:{port}".format(ip_domain=self.ip_domain, port=self.port, e=e)
            logger.info(error_msg)

    def exec_cmd(self, go_init, cmd):
        """
        used : to execute cmd
        :param go_init : instance of paramiko ssh agent
        :param cmd : executable cmd
        """
        # execute cmd
        try:
            stdin, stdout, stderr = go_init.exec_command(cmd)
            done_flag = stdout.channel.recv_exit_status()
            stdout_info = stdout.read()
            go_init.close()

            if done_flag == 0:
                # return normal info
                exec_info = "[action]:execute cmd" \
                            "[status]:OK" \
                            "[done_flag]:{done_flag}" \
                            "[stdout]:{stdout}" \
                            "[ip_domain]:{ip_domain}" \
                            "[port]:{port}" \
                            "[cmd]:{cmd}".format(ip_domain=self.ip_domain, port=self.port, stdout=stdout_info,
                                                 done_flag=done_flag, cmd=cmd)
                logger.info(exec_info)
                return done_flag, stdout_info

            else:
                error_msg = "[action]:execute cmd" \
                            "[status]:FAIL" \
                            "[done_flag]:{done_flag}" \
                            "[stdout]:{stdout}" \
                            "[ip_domain]:{ip_domain}" \
                            "[port]:{port}" \
                            "[cmd]:{cmd}".format(ip_domain=self.ip_domain, port=self.port, stdout=stdout_info,
                                                 done_flag=done_flag, cmd=cmd)
                logger.error(error_msg)
                return done_flag, stdout_info

        except Exception, e:
            error_msg = "[action]:execute cmd" \
                        "[status]:FAIL" \
                        "[Errorcode]:{e}" \
                        "[ip_domain]:{ip_domain}" \
                        "[port]:{port}" \
                        "[cmd]:{cmd}".format(ip_domain=self.ip_domain, port=self.port,
                                             cmd=cmd, e=e)
            logger.error(error_msg)
            return 2, 'exec_cmd error'


if __name__ == '__main__':

    paramikoconfig = {'username': 'root',
                      'password': 'tfkj705',
                      'key_file': ''}

    miko = MyMiko('192.168.41.40', 22, paramikoconfig)
    #print miko.go()
    print 'xxxxxxx', miko.exec_cmd(miko.go(), 'mkdir /zhiha/test_paramiko6')
    #print 'xxxxxxx', miko.exec_cmd(miko.go(), 'cd /zhihao && ls -l udate*')
    #(0,'text') --> OK
    #(1,)--> bad (mistake cmd)
    #(2,)--> bad (no file)

    '''
    print MyMiko('192.168.41.40', 22, paramikoconfig).__class__
    print MyMiko('192.168.41.40', 22, paramikoconfig).__dict__
    '''

    #import MyGO
    #help(MyGO)









