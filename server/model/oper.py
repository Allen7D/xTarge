# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from pymongo import MongoClient
import time

db_oper = MongoClient().safe_protocol.oper

class Oper:
  @staticmethod
  def get_oper():
    oper_list = []
    opers = db_oper.find()
    for oper in opers:
      oper = {
        'user_id': oper.get('user_id'),
        'username': oper.get('user_name'),
        'time': oper.get('time'),
        'protocol_type': oper.get('protocol_type'),
        'op': oper.get('oper')
      }
      oper_list.append(oper)
    return {'opers': oper_list}

  @staticmethod
  def create_oper(oper):
    oper = {
      'user_id': oper['user_id'],
      'user_name': oper['username'],
      'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
      'protocol_type': oper['protocol_type'],
      'oper': oper['oper']
    }
    print('hehe'*10, oper)
    db_oper.insert(oper)



