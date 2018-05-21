# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/20.
"""
from flask import request, jsonify

from . import api
from server.model.cmnt import Cmnt
from server.model.util import Utility

__author__ = 'Alimazing'


@api.route('/api/v1.0/cmnts', methods=['GET'])
def get_cmnts():
    # data = Cmnt.get_cmnt()
    data = Utility.get_data(table="cmnt")
    return jsonify(data), 200
