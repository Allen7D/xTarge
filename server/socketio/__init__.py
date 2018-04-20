# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/20.
"""
from flask_socketio import SocketIO
from flask import request

from server.utils import util

__author__ = 'Alimazing'

iec104_json_path = "./server/data/iec104_server.json" # 所有操作和读取所涉及的路径，都是相对于targeman.py
iec104_json_dst = "/etc/safe/iec104.json"
modbus_json_path = "./server/data/modbus_server.json"
modbus_json_dst = "/etc/safe/modbus.json"

socketio = SocketIO()

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
    json_path, json_dst = iec104_json_path, iec104_json_dst
  elif data['type'] == 'modbus':
    json_path, json_dst = modbus_json_path, modbus_json_dst
  else:
    socketio.emit("setting", "Failed!")
    print("identifing type error!")

  try:
    with open(json_path, "w") as f:
      f.write(data["json"])
    util.copy_file(src=json_path, dst=json_dst)
    socketio.emit("setting", "Success!")
    print("Receive json file")
  except:
    socketio.emit("setting", "Failed!")
    print("Writing file error!")
