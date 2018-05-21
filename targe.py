# _*_ coding: utf-8 _*_
"""
  Created by Alimazing on 2018/4/20.
"""
import signal, sys
from threading import Thread
from server.utils.watcher import Watcher
from server import create_app, Monitor

__author__ = 'Alimazing'

socketio, app = create_app()


def main_server(port=5000):
    socketio.run(app, host="0.0.0.0", port=port)

if __name__ == '__main__':
    Watcher()
    iec104_monitor = Monitor()
    modbus_monitor = Monitor()

    try:
        thr_server = Thread(target=main_server, name='main_server', args=())
        thr_iec104 = Thread(target=iec104_monitor.monitor_server,
                            name='iec104_monitor_server', args=(8010, 'iec104', socketio))
        thr_modbus = Thread(target=modbus_monitor.monitor_server,
                            name='modbus_monitor_server', args=(8020, 'modbus', socketio))
        thr_list = []
        thr_list.append(thr_server)
        thr_list.append(thr_iec104)
        thr_list.append(thr_modbus)

        for thr in thr_list:
            thr.setDaemon(True)
            thr.start()

        for thr in thr_list:
            thr.join(2)

        while True:
            pass
    except Exception as e:
        print("Error: {0}".format(e))


