# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/19.
"""
from flask import json, request

from server.model.oper import Oper
from server.model.util import Utility
from . import api

__author__ = 'Alimazing'


@api.route('/api/v1.0/ops', methods=['GET'])
def get_oper():
    # data = Oper.get_oper()
    data = Utility.get_data(table="os")
    return json.dumps(data), 200


@api.route('/api/v1.0/ops', methods=['POST'])
def post_oper():
    op = {
        'user_id': request.form['user_id'],
        'username': request.form['username'],
        'protocol_type': request.form['protocol_type'],
        'op': request.form['op']
    }
    Oper.add_oper(op)
    return json.dumps({}), 200
