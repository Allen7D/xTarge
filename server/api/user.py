# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/19.
"""
from flask import request, json, jsonify
from server.model.user import User
from . import api
from server.model.util import Utility

__author__ = 'Alimazing'


@api.route('/api/v1.0/users', methods=['GET'])
def get_user():
    # data = User.get_user()
    data = Utility.get_data(table="user")
    return json.dumps(data), 200


@api.route('/api/v1.0/users', methods=['POST'])
def post_user():
    user = {'id': request.form['id'],
            'username': request.form['username'],
            'password': request.form['password'],
            'level': request.form['level'],
            }
    User.add_user(user)
    return jsonify({}), 200


@api.route('/api/v1.0/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    data = {
        'password': request.form['password'],
        'level': request.form['level']
    }
    print(data)
    User.modify_user(user_id, data)
    return jsonify({}), 200


@api.route('/api/v1.0/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    User.delete_user(user_id)
    return jsonify({}), 200
