# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from pymongo import MongoClient
import time

db_op = MongoClient().safe_protocol.os

class Oper:
  @staticmethod
  def get_oper():
    op_list = []
    ops = db_op.find()
    for op in ops:
      op = {
        'user_id': op.get('user_id'),
        'username': op.get('user_name'),
        'time': op.get('time'),
        'protocol_type': op.get('protocol_type'),
        'op': op.get('os')
      }
      op_list.append(op)
    return {'ops': op_list}

  @staticmethod
  def add_oper(op):
    op = {
      'user_id': op['user_id'],
      'user_name': op['username'],
      'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
      'protocol_type': op['protocol_type'],
      'os': op['op']
    }
    db_op.insert(op)



