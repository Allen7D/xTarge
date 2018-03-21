# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from pymongo import MongoClient

db_alert = MongoClient().safe_protocol.alert

def get_alerts():
  alert_list = []
  alerts = db_alert.find()
  for alert in alerts:
    alert = {
      'time': alert.get('time'),
      'alert_type': alert.get('alert')['type'],
      'message': alert.get('alert')['Message']
    }
    alert_list.append(alert)

  return {'alerts': alert_list}
