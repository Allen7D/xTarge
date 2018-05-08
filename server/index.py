# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from flask import Flask, render_template, request, json, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo import MongoClient
import threading
import socket
from select import select
import datetime
import random

import config
from model import db
from utils import util
from utils.watcher import Watcher

iec104_json_path = "./server/data/iec104_server.json"
iec104_json_dst = "/etc/safe/iec104.json"
modbus_json_path = "./server/data/modbus_server.json"
modbus_json_dst = "/etc/safe/modbus.json"

app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")
app.config.from_object(config)
cors = CORS(app, resources={"/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode="threading")

def is_alert_or_cmnt(dict_data):
    if 'Buffer' in dict_data:
        return 'cmnt'
    return 'alert'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
  (username, password) = (request.form['username'], request.form['password'])
  is_user = db.verify_user(username, password)
  if is_user:
    user = db.get_user(username)
    return json.dumps({
      '_id': user['_id'],
      'name': user['name'],
      'level': user['level']
    }), 200
  else:
    return json.dumps({'msg': '账号和密码不匹配', 'errorCode': 'error_args'}), 401


@app.route('/api/v1.0/users', methods=['GET'])
def api_get_users():
  data = db.get_users()
  return json.dumps(data), 200


@app.route('/api/v1.0/users', methods=['POST'])
def api_post_users():
  user = {'id': request.form['id'],
          'username': request.form['username'],
          'password': request.form['password'],
          'level': request.form['level'],
          }
  db.add_user(user)
  return jsonify({}), 200


@app.route('/api/v1.0/users/<user_id>', methods=['PUT'])
def api_put_users(user_id):
  data = {
    'password': request.form['password'],
    'level': request.form['level']
  }
  print(data)
  db.modify_user(user_id, data)
  return jsonify({}), 200


@app.route('/api/v1.0/users/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
  db.delete_user(user_id)
  return jsonify({}), 200


@app.route('/api/v1.0/ops', methods=['GET'])
def api_get_ops():
  data = db.get_operationes()
  return json.dumps(data), 200


@app.route('/api/v1.0/ops', methods=['POST'])
def api_post_ops():
  op = {
    'user_id': request.form['user_id'],
    'username': request.form['username'],
    'protocol_type': request.form['protocol_type'],
    'op': request.form['op']
  }
  db.add_operation(op)

  return json.dumps({}), 200

@app.route('/api/v1.0/alerts', methods=['GET'])
def api_get_alerts():
  data = db.get_alerts()
  return json.dumps(data), 200

@app.route('/api/v1.0/alerts/<protocol_type>', methods=['GET'])
def api_get_alerts_by_type(protocol_type):
  data = db.get_alerts(protocol_type)
  return json.dumps(data), 200

@app.route('/api/v1.0/data', methods=['GET'])
def api_get_data():
  data = {'data': random.randint(100, 200)}
  return json.dumps(data), 200

def main_server(port=5000):
  socketio.run(app, host="0.0.0.0", port=port)


def iec104_monitor_server(port=8010):
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
          ctx = util.deal_with_alert_data(data.strip())
          now = datetime.datetime.now()
          time = now.strftime('%Y-%m-%d %H:%M:%S')
          alert_or_cmnt = is_alert_or_cmnt(ctx)
          if alert_or_cmnt == 'alert':
            new_obj = {'type': 'iec104', 'message': ctx['Message'], 'time': time}
            MongoClient().safe_protocol.alert.insert(new_obj)
            socketio.emit("alert", {'type': 'iec104', 'message': ctx['Message'], 'time': time})
          else:
           buffer, ip = ctx['Buffer'], ctx['client Ip']
           new_obj = {'buffer': buffer, 'ip': ip, 'time': time}
           MongoClient().safe_protocol.cmnt.insert(new_obj)
           socketio.emit("ctx", {'buffer': buffer, 'ip': ip, 'time': time})


def modbus_monitor_server(port=8020):
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
          ctx = util.deal_with_alert_data(data.strip())
          print('-----'*10, ctx)
          now = datetime.datetime.now()
          time = now.strftime('%Y-%m-%d %H:%M:%S')
          alert_or_cmnt = is_alert_or_cmnt(ctx)
          if alert_or_cmnt == 'alert':
            new_obj = {'type': 'modbus', 'message': ctx['Message'], 'time': time}
            socketio.emit("alert", new_obj)
            MongoClient().safe_protocol.alert.insert(new_obj)
          else:
            buffer, ip = ctx['Buffer'], ctx['client Ip']
            new_obj = {'buffer': buffer, 'ip': ip, 'time': time}
            socketio.emit("ctx", new_obj)
            MongoClient().safe_protocol.cmnt.insert(new_obj)

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
    util.copy_file(src=json_path, dst=json_dst)
    print("Receive json file")

    socketio.emit("setting", "Success!")
  except:
    socketio.emit("setting", "Failed!")
    print("Writing file error!")


if __name__ == '__main__':

  Watcher()

  t1 = threading.Thread(target=main_server, name='main_server', args=())
  t2 = threading.Thread(target=iec104_monitor_server, name='iec104_monitor_server', args=())
  t3 = threading.Thread(target=modbus_monitor_server, name='modbus_monitor_server', args=())

  t1.start()
  t2.start()
  t3.start()

  t1.join()
  t2.join()
  t3.join()
