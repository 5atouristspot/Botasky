#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-8-29


@module: api_0_1/moosefs
@used: api 1.0.0/moosefs moniter
"""

from flask import Blueprint
api = Blueprint('api_mfs', __name__)

from . import mfsmaster
from . import mfsmetalogger
from . import mfschunkserver
from . import mfscgiserv
from . import mfsmount

__all__ = ['']
__author__ = 'zhihao'