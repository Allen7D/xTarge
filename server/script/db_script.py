#!/usr/bin/env python
# coding:utf-8
'''
  首次安装项目，用于初始化MongoDB的user信息
'''

from werkzeug.security import generate_password_hash
from flask_script import Manager
import time

from model.db import db_user, db_op, db_alert

LEVEL1, LEVEL2, LEVEL3 = 'A', 'B', 'C'
register_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
DBManager = Manager()

@DBManager.command
def initUser():
  db_user.drop()
  users = [
    {'id': 100001, 'name': 'supadmin', 'password': generate_password_hash('supadmin'), 'level': LEVEL1, 'register_time': register_time},
    {'id': 100002, 'name': 'admin', 'password': generate_password_hash('admin'), 'level': LEVEL2, 'register_time': register_time},
    {'id': 100003, 'name': 'admin1', 'password': generate_password_hash('admin1'), 'level': LEVEL2, 'register_time': register_time},
    {'id': 100004, 'name': 'admin2', 'password': generate_password_hash('admin2'), 'level': LEVEL2, 'register_time': register_time},
    {'id': 100005, 'name': 'admin3', 'password': generate_password_hash('admin3'), 'level': LEVEL2, 'register_time': register_time},
    {'id': 100006, 'name': 'gushenxing', 'password': generate_password_hash('gushenxing'), 'level': LEVEL3, 'register_time': register_time},
    {'id': 100007, 'name': 'dongdongwei', 'password': generate_password_hash('dongdongwei'), 'level': LEVEL3, 'register_time': register_time},
    {'id': 100008, 'name': 'cenliguang', 'password': generate_password_hash('cenliguang'), 'level': LEVEL3, 'register_time': register_time},
    {'id': 100009, 'name': 'wangconger', 'password': generate_password_hash('wangconger'), 'level': LEVEL3, 'register_time': register_time},
  ]
  for user in users:
    db_user.insert(
      {'_id': user['id'], 'name': user['name'], 'password': user['password'], 'level': user['level'], 'register_time': user['register_time']})

  print('数据库：用户信息初始化完成！')


@DBManager.command
def showUser():
  print('数据库：显示所有用户信息！')
  users = db_user.find({})
  for user in users:
    print(user)


@DBManager.command
def wipeUser():
  db_user.drop()
  print('数据库：用户信息清空！')


@DBManager.command
def showOS():
  ops = db_op.find({})
  for op in ops:
    print(op)

@DBManager.command
def initAlert():
  db_alert.drop()
  alerts = [
    {"time": "2018-03-16 15:57:27", "alert": {"type": "iec104", "Message": "Access forbidden funcion code", "data": "1"}},
    {"time": "2018-03-16 15:59:40", "alert": {"type": "modbus", "Message": "Access forbidden funcion code", "data": "1"}},
    {"time": "2018-03-16 16:23:41", "alert": {"ip": "192.168.3.62", "Message": "Access forbidden ip&&mac ", "type": "modbus"}},
    {"time": "2018-03-16 16:25:29", "alert": {"type": "iec104", "Message": "Access forbidden funcion code", "data": "3"}},
    {"time": "2018-03-16 16:27:22", "alert": {"type": "iec104", "Message": "Access forbidden funcion code", "data": "3"}},
    {"time": "2018-03-16 16:30:44", "alert": {"Message": "Access forbiddened memory area", "type": "modbus", "   19": "   37"}},
    {"time": "2018-03-16 16:31:43", "alert": {"Message": "Access forbiddened memory area", "type": "modbus", "   19": "   37"}},
    {"time": "2018-03-16 16:31:44", "alert": {"Message": "Access forbiddened memory area", "type": "modbus", "   19": "   37"}},
    {"time": "2018-03-16 16:31:44", "alert": {"Message": "Access forbiddened memory area", "type": "modbus", "   19": "   37"}},
    {"time": "2018-03-16 16:37:36", "alert": {"type": "iec104", "Message": "Access forbidden funcion code", "data": "4"}},
    {"time": "2018-03-16 16:39:23", "alert": {"type": "modbus", "Message": "Access forbidden funcion code", "data": "5"}}
  ]
  for alert in alerts:
    db_alert.insert(
      {'time': alert['time'], 'alert': alert['alert']})

  print('数据库：alert信息初始化完成！')
