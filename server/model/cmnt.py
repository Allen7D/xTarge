# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/20.
"""

from pymongo import MongoClient

__author__ = 'Alimazing'

db_cmnt = MongoClient().safe_protocol.cmnt

class Cmnt:
  @staticmethod
  def get_cmnt():
    cmnt_list = []
    cmnts = db_cmnt.find()
    for cmnt in cmnts:
      cmnt = {
        'time': cmnt.get('time'),
        'buffer': cmnt.get('buffer'),
        'ip': cmnt.get('ip')
      }
      cmnt_list.append(cmnt)

    return {'cmnts': cmnt_list}

