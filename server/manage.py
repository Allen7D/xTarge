# !/usr/bin/env python
# _*_ coding: utf-8 _*_


from flask_script import Manager
from script.db_script import DBManager
from app import app

def manage(app):
  manager = Manager(app)
  manager.add_command('db', DBManager)
  manager.run()

if __name__ == '__main__':
  '''
    判断「是否为入口文件」
  '''
  manage(app)
