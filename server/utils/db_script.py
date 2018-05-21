#!/usr/bin/env python
# coding:utf-8
'''
  首次安装项目，用于初始化MongoDB的user信息
'''

from werkzeug.security import generate_password_hash
from flask_script import Manager
import time

from server.model import db_user, db_oper, db_alert, db_cmnt

LEVEL1, LEVEL2, LEVEL3 = 'A', 'B', 'C'
create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
DBManager = Manager()


@DBManager.command
def initUser():
    db_user.drop()
    users = [
        {'id': 100001, 'name': 'superadmin', 'password': generate_password_hash('superadmin'), 'level': LEVEL1,
         'create_time': create_time},
        {'id': 100002, 'name': 'admin', 'password': generate_password_hash('admin'), 'level': LEVEL2,
         'create_time': create_time},
        {'id': 100003, 'name': 'admin1', 'password': generate_password_hash('admin1'), 'level': LEVEL2,
         'create_time': create_time},
        {'id': 100004, 'name': 'admin2', 'password': generate_password_hash('admin2'), 'level': LEVEL2,
         'create_time': create_time},
        {'id': 100005, 'name': 'panxiao', 'password': generate_password_hash('panxiao'), 'level': LEVEL2,
         'create_time': create_time},
        {'id': 100006, 'name': 'gushenxing', 'password': generate_password_hash('gushenxing'), 'level': LEVEL3,
         'create_time': create_time},
        {'id': 100007, 'name': 'dongdongwei', 'password': generate_password_hash('dongdongwei'), 'level': LEVEL3,
         'create_time': create_time},
        {'id': 100008, 'name': 'cenliguang', 'password': generate_password_hash('cenliguang'), 'level': LEVEL3,
         'create_time': create_time},
        {'id': 100009, 'name': 'wangconger', 'password': generate_password_hash('wangconger'), 'level': LEVEL3,
         'create_time': create_time}
    ]
    for user in users:
        db_user.insert(
            {'_id': user['id'], 'name': user['name'], 'password': user['password'], 'level': user['level'],
             'create_time': user['create_time']})

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
def showOper():
    opers = db_oper.find({})
    for oper in opers:
        print(oper)


@DBManager.command
def wipeOper():
    db_oper.drop()
    print('数据库：操作日志清空！')


@DBManager.command
def initAlert():
    db_alert.drop()
    alerts = [
        {"time": "2018-03-11 15:57:27", "type": "iec104", "message": "Access forbidden funcion code"},
        {"time": "2018-03-12 15:59:40", "type": "modbus", "message": "Access forbidden funcion code"},
        {"time": "2018-03-13 06:23:41", "type": "modbus", "message": "Access forbidden ip&&mac"},
        {"time": "2018-03-14 16:25:29", "type": "iec104", "message": "Access forbidden funcion code"},
        {"time": "2018-03-15 07:27:22", "type": "iec104", "message": "Access forbidden funcion code"},
        {"time": "2018-03-16 11:30:44", "type": "modbus", "message": "Access forbiddened memory area"},
        {"time": "2018-03-17 08:21:43", "type": "modbus", "message": "Access forbiddened memory area"},
        {"time": "2018-03-18 16:11:44", "type": "modbus", "message": "Access forbiddened memory area"},
        {"time": "2018-03-19 22:01:44", "type": "modbus", "message": "Access forbiddened memory area"},
        {"time": "2018-03-20 15:07:36", "type": "iec104", "message": "Access forbidden funcion code"},
        {"time": "2018-03-21 13:29:23", "type": "modbus", "message": "Access forbidden funcion code"}
    ]
    for alert in alerts:
        db_alert.insert(
            {'time': alert['time'], 'type': alert['type'], 'message': alert['message']})

    print('数据库：alert信息初始化完成！')


@DBManager.command
def initCmnt():
    db_cmnt.drop()
    cmnts = [
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.148",
         "time": "2018-04-05 13:31:36"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.148",
         "time": "2018-04-06 07:04:08"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.148",
         "time": "2018-04-07 23:11:44"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.148",
         "time": "2018-04-08 15:12:49"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.148",
         "time": "2018-04-05 13:31:36"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.148",
         "time": "2018-05-06 07:04:08"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.149",
         "time": "2018-05-07 23:11:44"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.149",
         "time": "2018-05-08 15:12:49"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.149",
         "time": "2018-05-05 13:31:36"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.149",
         "time": "2018-05-06 07:04:08"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.149",
         "time": "2018-05-07 23:11:44"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.135",
         "time": "2018-05-18 15:12:49"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.135",
         "time": "2018-05-15 13:31:36"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.135",
         "time": "2018-05-16 07:04:08"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.135",
         "time": "2018-05-17 23:11:44"},
        {"buffer": "<00><02><00><00><00><06><FF><03><01><30><00><01>", "ip": "192.168.3.135",
         "time": "2018-05-18 15:12:49"}
    ]
    for cmnt in cmnts:
        db_cmnt.insert(
            {'time': cmnt['time'], 'buffer': cmnt['buffer'], 'ip': cmnt['ip']})

    print('数据库：通信操作信息初始化完成！')
