# !/usr/bin/env python
# _*_ coding: utf-8 _*_

# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from pymongo import MongoClient

db_alert = MongoClient().safe_protocol.alert

class Alert:
  @staticmethod
  def get_alert(protocol_type=None):
    alert_list = []
    alerts = db_alert.find()
    for alert in alerts:
      alert = {
        'time': alert.get('time'),
        'protocol_type': alert.get('alert')['type'],
        'message': alert.get('alert')['Message']
      }
      alert_list.append(alert)

    if protocol_type:
      alert_list = list(filter(lambda x: x['protocol_type'] == protocol_type, alert_list))
    return {'alerts': alert_list}



