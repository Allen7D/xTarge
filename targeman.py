# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/20.
"""
from threading import Thread

from server.utils.watcher import Watcher
from server import create_app
from server import monitor_server

__author__ = 'Alimazing'

socketio, app = create_app()

def main_server(port=5000):
  socketio.run(app, host="0.0.0.0", port=port)

if __name__ == '__main__':
  Watcher()

  main_server(port=5000)
  # thr_main = Thread(target=main_server, name='main_server', args=())
  thr_iec104 = Thread(target=monitor_server,
                      name='iec104_monitor_server', args=[8010, 'iec104', socketio])
  thr_modbus = Thread(target=monitor_server,
                      name='modbus_monitor_server', args=[8020, 'modbus', socketio])

  thr_iec104.start()
  thr_modbus.start()

  thr_iec104.join()
  thr_modbus.join()
