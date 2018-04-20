# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
from threading import Thread
import socket
from select import select
import datetime

import config
from pymongo import MongoClient
from utils import util
from utils.watcher import Watcher

from api import api
from web import web

iec104_json_path = "./server/data/iec104_server.json"
iec104_json_dst = "./server/etc/safe/iec104.json"
modbus_json_path = "./server/data/modbus_server.json"
modbus_json_dst = "./server/etc/safe/modbus.json"

app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")
app.register_blueprint(api)
app.register_blueprint(web)
app.config.from_object(config)
cors = CORS(app, resources={"/*": {"origins": "*"}})
socketio = SocketIO()
socketio.init_app(app, async_mode="threading")


def main_server(port=5000):
  socketio.run(app, host="0.0.0.0", port=port)


def monitor_server(port=8010, protocol_type='iec104'):
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
          alert_data = util.deal_with_alert_data(data.strip())
          alert_data['type'] = protocol_type
          now = datetime.datetime.now()
          time = now.strftime('%Y-%m-%d %H:%M:%S')

          MongoClient().safe_protocol.alert.insert({'alert': alert_data, 'time': time})
          socketio.emit("alert", alert_data)


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

  main_server()
  # thr_main = Thread(target=main_server, name='main_server', args=())
  thr_iec104 = Thread(target=monitor_server,
                      name='iec104_monitor_server', args=[8010, 'iec104'])
  thr_modbus = Thread(target=monitor_server,
                      name='modbus_monitor_server', args=[8020, 'modbus'])

  thr_iec104.start()
  thr_modbus.start()

  thr_iec104.join()
  thr_modbus.join()
