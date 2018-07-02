#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2018-01-09


@module: choice_collection_info_table
@used: used to choice collection info table
"""

import datetime


def get_table():
    #choice collection_info table
    now_year = datetime.datetime.now().year
    now_month =  datetime.datetime.now().month
    if now_month < 10 :
        collection_info = 'collection_info_' + str(now_year) + '0' + str(now_month)
    else:
        collection_info = 'collection_info_' + str(now_year) + str(now_month)

    return collection_info