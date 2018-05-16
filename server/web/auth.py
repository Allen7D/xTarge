# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/19.
"""
from flask import json, jsonify, request, render_template
from server.model.user import User
from . import web

__author__ = 'Alimazing'

@web.route('/', defaults={'path': ''})
@web.route('/<path:path>')
def index(path):
  return render_template("index.html")

@web.route('/login', methods=['POST'])
def login():
  (username, password) = (request.form['username'], request.form['password'])
  is_user = User.verify_user(username, password)
  if is_user:
    user = User.get_user_by_name(username)
    return jsonify({
      '_id': user['_id'],
      'name': user['name'],
      'level': user['level']
    }), 200
  else:
    return json.dumps({'msg': '账号和密码不匹配', 'errorCode': 'error_args'}), 401


@web.route('/modbus', methods=['GET'])
def modbus():
  return render_template("index.html")


@web.route('/iec104', methods=['GET'])
def iec104():
  return render_template("index.html")


@web.route('/admin/user', methods=['GET'])
def admin_auth():
  return render_template("index.html")


@web.route('/admin/alert', methods=['GET'])
def admin_alert():
  return render_template("index.html")


@web.route('/admin/oper', methods=['GET'])
def admin_oper():
  return render_template("index.html")
