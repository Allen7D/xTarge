# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/19.
"""
__author__ = 'Alimazing'

from flask import Blueprint

api = Blueprint('api', __name__)

from server.api import user
from server.api import alert
from server.api import oper
from server.api import cmnt
