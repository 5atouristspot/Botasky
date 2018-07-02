#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-7-6


@module: MyFILE
@used: find file 's absolute path
"""


import os
import fnmatch

__all__ = ['recursiveSearchFile']
__author__ = 'zhihao'


#project 's absolute path
project_abdir = '/Botasky/boird'

def recursiveSearchFile(searchPath, partInfo):
    wantFilesPath = []
    for (dirPath, dirNames, fileNames) in os.walk(searchPath):
        wantFilesPath += [os.path.join(dirPath, fileName) for fileName in fileNames if
                          fnmatch.fnmatch(os.path.join(dirPath, fileName), partInfo)]
    return wantFilesPath



if __name__ == "__main__":
    fileList = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
    print fileList
    paramiko_log = recursiveSearchFile(project_abdir, '*paramiko.log')[0]
    print paramiko_log
    #for path in fileList:
    #    print path
