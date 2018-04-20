#!/usr/bin/env python
# coding:utf-8

from flask import Flask, render_template, session, request,redirect,url_for,flash
from flask_socketio import SocketIO, emit
from flask_login import login_user, logout_user, login_required, current_user, LoginManager, UserMixin, AnonymousUserMixin
from flask_cors import CORS
from .func import *
from .utils.watcher import Watcher

import json
import threading
import os
import socket
from select import select
import datetime

iec104_json_path = "./server/data/iec104_server.json"
iec104_json_dst = "/etc/safe/iec104.json"
modbus_json_path = "./server/data/modbus_server.json"
modbus_json_dst = "/etc/safe/modbus.json"

async_mode = "threading"

app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, resources={"/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode=async_mode)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = MongoClient().safe_protocol.user.find_one({'_id': user_id})
    temp = Temp(user.get('_id'), user.get('name'), user.get('password'), user.get('level'))
    return temp

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'] # request.args.get('')获取URL中的get请求的参数, request.form['']获取POST过来的表单
    userpw = request.form['password']

    user = query(username, 'name')
    if user is not None and verify_password(user.get('password'), userpw) :
        name = user.get('name')
        password = user.get('password')
        level = user.get('level')
        u_id = user.get('_id')

        temp = Temp(u_id, name, password, level)

        login_user(temp)

        print(login_u(current_user))
        return login_u(current_user)

    return json.dumps([{'msg': '账号和密码不匹配'},{'errorCode':'error_args'}]), 401

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    session.pop('username', None)
    session.pop('password', None)
    return json.dumps({"result":True}), 200

@app.route('/api/users', methods=['POST'])
@admin_required
def register():
    #return 'register'
    data = register_form()
    admin_pw = request.form['admin_password']

    new_user = json.loads(data)
    #return new_user['name']
    if query(new_user['name'], 'name') != None:
        return 'name has already exist'

    tag = request.args.get('tag')
    admin_user = query(tag, 'id')
    admin_level = admin_user.get('level')
    admin_password = admin_user.get('password')

    if not verify_password(admin_password, admin_pw):
        return json.dumps([{'msg': 'admin password error'},{'errorCode':'error_args'}]), 400

    if admin_level == 'A':
        return insert(new_user)
    if admin_level == 'B' and new_user['level'] == 'C':
        return insert(new_user)
    return json.dumps([{'msg': 'need_permission'},{'errorCode':'need_permission'}]), 401


@app.route('/api/users',methods = ['DELETE'])
@admin_required
def delete():
    tag = request.args.get('tag')
    admin_user = query(tag, 'id')
    admin_level = admin_user.get('level')
    admin_password = admin_user.get('password')

    user_id = request.form['user_id']
    admin_pw = request.form['admin_password']

    if not verify_password(admin_password, admin_pw):
        return json.dumps([{'msg': 'admin password error'},{'errorCode':'error_args'}]), 400

    user = query(int(user_id), 'id')

    if user == None:
        return json.dumps([{'msg': 'no user'},{'errorCode':'error_args'}]), 400

    if admin_level >= user.get('level'):
        return json.dumps([{'msg': 'forbidden'},{'errorCode':'error_args'}]), 403

    return delete_user(user)


@app.route('/api/users', methods=['GET'])
def all_users():
    user_list = []
    users = MongoClient().safe_protocol.user.find()
    for user in users:
        user_list.append({'user_id': user.get('_id'), 'username': user.get('name'), 'level': user.get('level')})
    if len(user_list) == 1:
        return (json.dumps(user_list[0])), 200
    return json.dumps(user_list), 200

@app.route('/api/users', methods = ['PUT'])
@admin_required
def reset():
    tag = request.args.get('tag')
    admin_user = query(tag, 'id')
    admin_level = admin_user.get('level')
    admin_password = admin_user.get('password')

    user_id = request.form['user_id']
    try:
        new_set = request.form['new_password']
        flag = 'pw'
    except:
        new_set = request.form['new_level']
        flag = 'level'
    admin_pw = request.form['admin_password']

    if not verify_password(admin_password, admin_pw):
        return json.dumps([{'msg': 'admin password error'},{'errorCode':'error_args'}]), 400

    if flag == 'level' and admin_level != 'A':
        return json.dumps([{'msg': 'forbidden'},{'errorCode':'error_args'}]), 403

    user = query(int(user_id), 'id')

    if user == None:
        return json.dumps([{'msg': 'no user'},{'errorCode':'error_args'}]), 400

    if admin_level >= user.get('level'):
        return json.dumps([{'msg': 'forbidden'},{'errorCode':'error_args'}]), 403

    return update_set(user, new_set, flag)
################################################

@app.route("/api/action_id", methods = ['GET'] )
def action_id():
    info_list = []
    user_id = request.form['user_id']
    #return user_id
    try:
        info_s = MongoClient().safe_protocol.os.find({'user_id':int(user_id)})
    except:
        return json.dumps([{'msg': 'no user'},{'errorCode':'error_args'}]), 400

    for info in info_s:
        data = {"username":info.get('user_name'), "user_id":info.get('user_id'), "os":info.get('os'), "time":info.get('time')}
        info_list.append(data)

    if len(info_list) == 1:
        return (json.dumps(info_list[0])), 200

    return json.dumps(info_list), 200

@app.route("/api/action_time", methods = ['GET'] )
def action_time():
    info_list = []

    s_time = request.form['s_time']
    e_time = request.form['e_time']

    if e_time <= s_time:
        return json.dumps([{'msg': 'time error'},{'errorCode':'error_args'}]), 400

    info_s = MongoClient().safe_protocol.os.find({"time":{"$gte":s_time, "$lt":e_time}})
    for info in info_s:
        data = {"username":info.get('user_name'), "user_id":info.get('user_id'), "os":info.get('os'), "time":info.get('time')}
        info_list.append(data)

    if len(info_list) == 1:
        return (json.dumps(info_list[0])), 200

    return json.dumps(info_list), 200

@app.route("/api/alert", methods = ['GET'] )
def alert():
    info_list = []

    info_s = MongoClient().safe_protocol.alert.find()

    for info in info_s:
        data = {"alert":info.get('alert'), "time":info.get('time')}
        info_list.append(data)

    if len(info_list) == 1:
        return (json.dumps(info_list[0])), 200

    return json.dumps(info_list), 200


########################################################################
def deal_with_alert_data(d):
    d1 = d.split("|")
    d2 = [s.split("-") for s in d1]
    return dict(d2)

def main_server(port=5000):
    socketio.run(app, host="0.0.0.0", port=port)

def iec104_monitor_server(port=8000):
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("0.0.0.0", port))
    s.listen(10)
    s.setblocking(False)
    inputs = []
    inputs.append(s)
    address = dict()

    while 1:
        rs, ws, es = select(inputs, [], [], 1)
        for r in rs:
            if r is s:
                conn, addr = s.accept()
                print("Client {0} connected !".format(addr))
                address[conn] = addr
                inputs.append(conn)
            else:
                data = r.recv(1024)
                if not data:
                    print("Client {0} disconnected !".format(address[r]))
                    address.pop(r)
                    inputs.remove(r)
                else:
                    d = deal_with_alert_data(data.strip())
                    d['type'] = 'iec104'
                    now = datetime.datetime.now()
                    time = now.strftime('%Y-%m-%d %H:%M:%S')

                    MongoClient().safe_protocol.alert.insert({'alert':d, 'time':time})
                    socketio.emit("alert", d)

def modbus_monitor_server(port=8111):
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("0.0.0.0", port))
    s.listen(10)
    s.setblocking(False)
    inputs = []
    inputs.append(s)
    address = dict()

    while 1:
        rs, ws, es = select(inputs, [], [], 1)
        for r in rs:
            if r is s:
                conn, addr = s.accept()
                print("Client {0} connected !".format(addr))
                address[conn] = addr
                inputs.append(conn)
            else:
                data = r.recv(1024)
                if not data:
                    print("Client {0} disconnected !".format(address[r]))
                    address.pop(r)
                    inputs.remove(r)
                else:
                    d = deal_with_alert_data(data.strip())
                    d['type'] = 'modbus'
                    now = datetime.datetime.now()
                    time = now.strftime('%Y-%m-%d %H:%M:%S')

                    MongoClient().safe_protocol.alert.insert({'alert':d, 'time':time})
                    socketio.emit("alert", d)

def deal_with_file(src, dst):
    cmd = "cp " + src+ " " + dst
    os.system(cmd)

def deal_with_json_data(dst):
    with open(dst, 'r') as f:
        content = json.load(f)
    return content



@socketio.on('connect')
def test_connect():
    print("Client connected!")
    try:
        iec104_file = open(iec104_json_path, "r")
        iec104_config = iec104_file.read()
        iec104_file.close()

        modbus_file = open(modbus_json_path, "r")
        modbus_config = modbus_file.read()
        modbus_file.close()

        socketio.emit("init", {"iec104": iec104_config, "modbus": modbus_config})
    except:
        socketio.emit("init", {"iec104": "{}", "modbus": "{}"})
        print("Loading file error!")


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on("setting")
def receive_json(data):
    if data['type'] == 'iec104':
        json_path = iec104_json_path
        json_dst = iec104_json_dst
    elif data['type'] == 'modbus':
        json_path = modbus_json_path
        json_dst = modbus_json_dst
    else:
        socketio.emit("setting", "Failed!")
        print("identifing type error!")

    try:
        with open(json_path, "w") as f:
            f.write(data["json"])
        deal_with_file(src=json_path, dst=json_dst)
        print("Receive json file")

        now = datetime.datetime.now()
        time = now.strftime('%Y-%m-%d %H:%M:%S')

        user_name = data['user_name'] # current_user.name
        user_id = data['user_id'] # current_user.id
        MongoClient().safe_protocol.os.insert({'user_id':user_id, 'user_name':user_name, 'time':time, 'os':deal_with_json_data(dst=json_dst)})
        socketio.emit("setting", "Success!")
    except:
        socketio.emit("setting", "Failed!")
        print("Writing file error!")


if __name__ == '__main__':

    Watcher()

    t1 = threading.Thread(target=main_server, args=())
    t2 = threading.Thread(target=iec104_monitor_server, args=())
    t3 = threading.Thread(target=modbus_monitor_server, args=())

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

