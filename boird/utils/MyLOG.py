#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-3-15


@module: MyLOG
@used: print log to console or file
"""


from logging.handlers import RotatingFileHandler
import time
import logging
import threading
import ConfigParser
import sys
reload(sys)

__all__ = ['MyLog']
__author__ = 'zhihao'


class MyLog:
    file_handler = ''

    def __init__(self, log_config, name):
        """
        used : init config and get value
        :param name : name of local file
        :param log_config : name of log config file
        """
        self.name = name
        self.logger = logging.getLogger(self.name)
        config = ConfigParser.ConfigParser()
        config.read(log_config)

        mythread = threading.Lock()
        mythread.acquire()  # thread lock

        self.log_file_path = config.get('LOGGING', 'log_file_path')
        self.maxBytes = config.get('LOGGING', 'maxBytes')
        self.backupCount = int(config.get('LOGGING', 'backupCount'))
        self.outputConsole_level = int(config.get('LOGGING', 'outputConsole_level'))
        self.outputFile_level = int(config.get('LOGGING', 'outputFile_level'))
        self.outputConsole = int(config.get('LOGGING', 'outputConsole'))
        self.outputFile = int(config.get('LOGGING', 'outputFile'))
        self.formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        self.console_handler = ''
        self.file_handler = ''

        mythread.release()  # thread lock relax

    def outputLog(self):
        """
        used : output log to console and file
        """
        if self.outputConsole == 1:
            # if true ,it should output log in console
            self.console_handler = logging.StreamHandler()
            self.console_handler.setFormatter(self.formatter)
            self.logger.setLevel(self.outputConsole_level)
            self.logger.addHandler(self.console_handler)
        else:
            pass

        if self.outputFile == 1:
            self.file_handler = RotatingFileHandler(self.log_file_path, maxBytes=10*1024*1024, backupCount=10)
            # define RotatingFileHandler, file output path, one file max byte, max backup number
            self.file_handler.setFormatter(self.formatter)
            self.logger.setLevel(self.outputFile_level)
            self.logger.addHandler(self.file_handler)

        else:
            pass

        return self.logger


if __name__ == '__main__':
    '''
    mylog = MyLog('logConfig.ini','jjjjj')
    logger = mylog.outputLog()
    logger.error("jjjjjjjjjjjjjjj")
    '''

    import MyLOG
    help(MyLOG)


