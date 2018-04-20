# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
import time

db_user = MongoClient().safe_protocol.user

class User:
  @staticmethod
  def get_user():
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

  @staticmethod
  def get_user_by_name(username):
    try:
      user = db_user.find_one({'name': username})
    except IOError:
      print('数据库不存在该用户')
    else:
      return user

  @staticmethod
  def add_user(user):
    user = {
      '_id': int(user['id']),
      'name': user['username'],
      'password': generate_password_hash(user['password']),
      'level': user['level'],
      'register_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    db_user.insert(user)

  @staticmethod
  def delete_user(user_id):
    db_user.remove({'_id': int(user_id)})

  @staticmethod
  def modify_user(user_id, data):
    (password, level) = (data['password'], data['level'])
    db_user.update({'_id': int(user_id)}, {'$set': {'password': generate_password_hash(password), 'level': level}})

  @classmethod
  def verify_user(cls, username, password):
    user = cls.get_user_by_name(username)
    is_user = cls.hash_check(user['password'], password)
    return is_user

  @staticmethod
  def hash_check(hashed_data, unhashed_data):
     is_equal = check_password_hash(hashed_data, unhashed_data)
     return is_equal

