# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/19.
"""
from flask import json, request

from server.model.oper import Oper
from server.model.util import Utility
from . import api

__author__ = 'Alimazing'


@api.route('/api/v1.0/opers', methods=['GET'])
def get_oper():
    # data = Oper.get_oper()
    data = Utility.get_data(table="oper")
    return json.dumps(data), 200


@api.route('/api/v1.0/opers', methods=['POST'])
def create_oper():
    print(request.form)
    oper = {
        'user_id': request.form['user_id'],
        'username': request.form['username'],
        'protocol_type': request.form['protocol_type'],
        'oper': json.loads(request.form['oper'])
    }
    Oper.create_oper(oper)
    return json.dumps({}), 200
