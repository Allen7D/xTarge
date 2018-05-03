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


def iec104_monitor_server(port=8010, protocol_type='iec104', socketio=None):
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
                    ctx = util.convert(data.strip())
                    is_alert_or_cmnt = is_alert_or_cmnt(ctx)
                    now = datetime.datetime.now()
                    time = now.strftime('%Y-%m-%d %H:%M:%S')
                    if is_alert_or_cmnt == 'alert':
                        ctx['type'] = protocol_type
                        new_obj = {'message': ctx['Message'], 'type': ctx['type'], 'time': time}
                        MongoClient().safe_protocol.alert.insert(new_obj)
                        socketio.emit("alert", new_obj)
                    else:
                        new_obj = {'buffer': ctx['Buffer'], 'ip': ctx['client Ip'], 'time': time}
                        MongoClient().safe_protocol.cmnt.insert(
                            {'buffer': ctx['Buffer'], 'ip': ctx['client Ip'], 'time': time})
                        socketio.emit("ctx", new_obj)


def modbus_monitor_server(port=8020, protocol_type='modbus', socketio=None):
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
                    ctx = util.convert(data.strip())
                    is_alert_or_cmnt = is_alert_or_cmnt(ctx)
                    now = datetime.datetime.now()
                    time = now.strftime('%Y-%m-%d %H:%M:%S')
                    if is_alert_or_cmnt == 'alert':
                        ctx['type'] = protocol_type
                        new_obj = {'message': ctx['Message'], 'type': ctx['type'], 'time': time}
                        MongoClient().safe_protocol.alert.insert(new_obj)
                        socketio.emit("alert", new_obj)
                    else:
                        new_obj = {'buffer': ctx['Buffer'], 'ip': ctx['client Ip'], 'time': time}
                        MongoClient().safe_protocol.cmnt.insert(
                            {'buffer': ctx['Buffer'], 'ip': ctx['client Ip'], 'time': time})
                        socketio.emit("ctx", new_obj)


def is_alert_or_cmnt(dict_data):
    if 'Buffer' in dict_data:
        return 'cmnt'
    return 'alert'
