#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-8-29


@module: api_0_1/keepalived
@used: api 1.0.0/keepalived moniter
"""

from flask import Blueprint
api = Blueprint('api_keepalived', __name__)

from . import keepalive
from . import vip

__all__ = ['']
__author__ = 'zhihao'