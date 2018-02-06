#!/usr/bin/env python
# coding:utf-8
from flask import Flask, render_template, session, request,redirect,url_for,flash
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap
from flask_login import login_user, logout_user, login_required, current_user, LoginManager, UserMixin, AnonymousUserMixin
from flask_cors import CORS
from forms import LoginForm, RegistrationForm, RegistrationForm2, ResetForm
from bson.objectid import ObjectId
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

import json
import signal
import sys
import threading
import os
import socket
from select import select
import datetime
import time

iec104_json_path = "./data/iec104_server.json"
iec104_json_dst = "/etc/safe/iec104.json"
modbus_json_path = "./data/modbus_server.json"
modbus_json_dst = "/etc/safe/modbus.json"

async_mode = "threading"

app = Flask(__name__, static_folder="./dist/static", static_url_path="", template_folder="./dist")
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, resources={"/*": {"origins": "*"}})
bootstrap = Bootstrap(app)
socketio = SocketIO(app, async_mode=async_mode)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

class Temp(UserMixin):
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, u_id, name, password, level):
        self.id =u_id
        self.name = name
        self.password = password
        self.level = level

    def __repr__(self):
        return self.name

    def get_id(self):
        return self.id

    def is_admin(self):
        if self.level == 'C':
            return False

        if self.level == 'A' or 'B':
            return True

def encrypt_passowrd(password):
    return generate_password_hash(password)


def verify_password(user_password, password):
    return check_password_hash(user_password, password)

def str_to_dict(s):
    exec("c=" + s)
    return c

@login_manager.user_loader
def load_user(user_id):
    user = MongoClient().safe_protocol.user.find_one({'_id': user_id})
    temp = Temp(user.get('_id'), user.get('name'), user.get('password'), user.get('level'))
    return temp

# @app.route("/", methods=['GET', 'POST'])
@app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
def index(path):
    return render_template("index.html")
    # return redirect(url_for('login'))

@app.route("/management", methods=['GET', 'POST'])
@login_required
def management():
    return render_template('html/management.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    username = request.form['username'] # args.get('***')获取URL中的get请求的参数, form获取POST过来的表单
    userpw = request.form['pass']
    print('hehehe')

    user = MongoClient().safe_protocol.user.find_one({'name':username})
    if user is not None and verify_password(user.get('password'), userpw) :
        name = user.get('name')
        password = user.get('password')
        level = user.get('level')
        u_id = user.get('_id')

        temp = Temp(u_id, name, password, level)

        login_user(temp)
        level = current_user.level
        result = current_user.is_admin()

        if result == True:
            return json.dumps([{'id': u_id, 'username': name, 'level': level}]), 200

    return json.dumps([{'msg': '账号和密码不匹配'}]), 401.1

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    session.pop('password', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    user_id = request.args.get('id')
    username = request.args.get('name')
    userpw = request.args.get('pw')
    e_password = encrypt_passowrd(userpw)
    userlevel = request.args.get('level')

    result = False
    level = current_user.level
    result = current_user.is_admin()
    if result == False:
        return 'you are not allowed'

    if result == True:
        user = MongoClient().safe_protocol.user.find_one({'name':username})
        if user != None:
            return 'name has already exist'

        if level == 'A':
            MongoClient().safe_protocol.user.insert({'_id':int(user_id),'name':username,'password':e_password,'level':userlevel})
            return 'success'
        if level == 'B':
            userlevel = 'C'
            MongoClient().safe_protocol.user.insert({'_id':int(user_id),'name':username,'password':e_password,'level':userlevel})
            return 'success'

@app.route('/delete')
@login_required
def delete():
    result = current_user.is_admin()
    user_id = request.args.get('id')
    level = current_user.level
    delete_user = MongoClient().safe_protocol.user.find_one({'_id':int(user_id)})

    if result == False:
        return 'you are not allowed'
    else:
        if delete_user == None:
            return 'the user is not exist'

        if level == 'A':
            MongoClient().safe_protocol.user.remove({'_id':int(user_id)})
            return 'delete success, return manage-user.html'
        elif level == 'B':
            delete_level = delete_user.get('level')
            if delete_level == 'C':
                MongoClient().safe_protocol.user.remove({'_id':int(user_id)})
                return 'delete success, return manage-user.html'
            else:
                return 'you can\'t delete admin-user'


@app.route('/api/all_users', methods=['GET'])
def all_users():
    # result = current_user.is_admin()
    # if result == False:
    #     return 'you are not allowed'
    user_list = []
    users = MongoClient().safe_protocol.user.find()
    for user in users:
        user_list.append({'id': user.get('_id'), 'username': user.get('name'), 'level': user.get('level')})
    return json.dumps(user_list), 200


@app.route('/reset_password', methods = ['GET', 'POST'])
@login_required
def reset_password():
    user_id = request.args.get('id')
    new_userpw = request.args.get('pw')
    e_password = encrypt_passowrd(new_userpw)

    level = current_user.level
    result = current_user.is_admin()
    login_id = current_user.id


    user = MongoClient().safe_protocol.user.find_one({'_id':int(user_id)})

    if result == False:
        if str(user_id) != str(login_id):
            return 'you can\'t reset other'

    if result == True:
        if user is None:
            return 'user_id is invalid!  please check your user_id'

        if level == 'B':
            if user.get('level') == 'A':
                return 'you can\'t reset super-admin'
            if user.get('level') == 'B':
                if str(user_id) != str(login_id):
                    return 'you can\'t reset other admin'

    MongoClient().safe_protocol.user.update({'_id':int(user_id)},{'$set':{'password':e_password}})
    return 'reset success, return <manage-user.html>'

    return render_template('html/reset.html', form=form)

@app.route('/reset_level', methods = ['GET', 'POST'])
@login_required
def reset_level():
    reset_id = request.args.get('id')
    reset_level = request.args.get('level')

    level = current_user.level
    result = current_user.is_admin()
    login_id = current_user.id

    if reset_level != 'B' and reset_level !='C':
        return 'error'

    user = MongoClient().safe_protocol.user.find_one({'_id':int(reset_id)})

    if level != 'A':
        return 'you can\'t reset other'
    if user is None:
        return 'user_id is invalid!  please check your user_id'


    MongoClient().safe_protocol.user.update({'_id':int(reset_id)},{'$set':{'level':reset_level}})
    return 'reset success, return <manage-user.html>'

@app.route("/action_name", methods = ['GET', 'POST'] )
@login_required
def action_name():
    result = current_user.is_admin()
    if result == False:
        return 'you are not allowed'
    info_list = []
    name = request.args.get('name')
    info_s = MongoClient().safe_protocol.os.find({'user_name':name})
    for info in info_s:
        info_list.append([info.get('user_name'),info.get('user_id'),info.get('os'),info.get('time')])
    return json.dumps(info_list)

@app.route("/action_time", methods = ['GET', 'POST'] )
@login_required
def action_time():
    result = current_user.is_admin()
    if result == False:
        return 'you are not allowed'
    info_list = []
    s_time = request.args.get('s_time')
    e_time = request.args.get('e_time')
    info_s = MongoClient().safe_protocol.os.find({"time":{"$gte":s_time, "$lt":e_time}})
    for info in info_s:
        info_list.append([info.get('user_name'),info.get('user_id'),info.get('os'),info.get('time')])
    return json.dumps(info_list)




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

        user_name = current_user.name
        user_id = current_user.id
        MongoClient().safe_protocol.os.insert({'user_id':user_id, 'user_name':user_name, 'time':time, 'os':deal_with_json_data(dst=json_dst)})
        socketio.emit("setting", "Success!")
    except:
        socketio.emit("setting", "Failed!")
        print("Writing file error!")

class Watcher():
    # 服务器监控，用于关闭
    def __init__(self):
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass


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
