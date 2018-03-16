# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
import time

db_user = MongoClient().safe_protocol.user
db_os = MongoClient().safe_protocol.os


def get_users():
  user_list = []
  users = db_user.find()
  for user in users:
    user_list.append({
      'user_id': user.get('_id'),
      'username': user.get('name'),
      'level': user.get('level'),
      'register_time': user.get('register_time')
    })

  return {'users': user_list}


def get_user(username):
  try:
    user = db_user.find_one({'name': username})
  except IOError:
    print('数据库不存在该用户')
  else:
    return user


def add_user(user):
  user = {
    '_id': int(user['id']),
    'name': user['username'],
    'password': generate_password_hash(user['password']),
    'level': user['level'],
    'register_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
  }
  db_user.insert(user)


def delete_user(user_id):
  db_user.remove({'_id': int(user_id)})


def modify_user(user_id, data):
  (password, level) = (data['password'], data['level'])
  db_user.update({'_id': int(user_id)}, {'$set': {'password': generate_password_hash(password), 'level': level}})


def verify_user(username, password):
  user = get_user(username)
  is_user = hash_check(user['password'], password)
  return is_user


def hash_check(hashed_data, unhashed_data):
   is_equal = check_password_hash(hashed_data, unhashed_data)
   return is_equal


'''
  「OS操作」数据
'''
def get_operationes():
  op_list = []
  ops = db_os.find()
  for op in ops:
    op = {
      'user_id': op.get('user_id'),
      'username': op.get('user_name'),
      'time': op.get('time'),
      'op': op.get('os')
    }
    op_list.append(op)

  return {'ops': op_list}

def add_operation(op):
  op = {
    'user_id': op['user_id'],
    'user_name': op['username'],
    'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    'protocol_type': op['protocol_type'],
    'os': op['op']
  }
  db_os.insert(op)


'''
  报警数据
'''

