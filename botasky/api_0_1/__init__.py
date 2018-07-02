#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-7-04


@module: api_0_1
@used: api 1.0.0
"""



from flask import Blueprint
api = Blueprint('api', __name__)

from . import register_verify_user

__all__ = ['']
__author__ = 'zhihao'