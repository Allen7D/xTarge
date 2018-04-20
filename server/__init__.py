# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/20.
"""

from flask import Flask
from flask_cors import CORS
import socket
from select import select
import datetime
from pymongo import MongoClient

from server.utils import util
from server.socketio import socketio

__author__ = 'Alimazing'


def create_app():
  app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")
  app.config.from_object('server.config')
  register_blueprint(app)

  cors = CORS()
  cors.init_app(app, resources={"/*": {"origins": "*"}})

  socketio.init_app(app, async_mode="threading")

  return socketio, app

def register_blueprint(app):
  from server.web import web
  from server.api import api
  app.register_blueprint(web)
  app.register_blueprint(api)


def monitor_server(port=8010, protocol_type='iec104', socketio=None):
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
        print('-----'*5)
        print('log_content:', data)
        print('-----'*5)
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


