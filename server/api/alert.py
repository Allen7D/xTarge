# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/19.
"""
from flask import json

from . import api
from server.model.alert import Alert

__author__ = 'Alimazing'

@api.route('/api/v1.0/alerts', methods=['GET'])
def get_alerts():
  data = Alert.get_alert()
  return json.dumps(data), 200

@api.route('/api/v1.0/alerts/<protocol_type>', methods=['GET'])
def get_alerts_by_type(protocol_type):
  data = Alert.get_alert(protocol_type)
  return json.dumps(data), 200
