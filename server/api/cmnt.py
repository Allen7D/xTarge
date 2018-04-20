# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/20.
"""
from flask import json

from . import api
from server.model.cmnt import Cmnt
__author__ = 'Alimazing'

@api.route('/api/v1.0/cmnts', methods=['GET'])
def get_alerts():
  data = Cmnt.get_cmnt()
  return json.dumps(data), 200
