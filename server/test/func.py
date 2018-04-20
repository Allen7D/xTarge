#!/usr/bin/env python
# coding:utf-8
import json

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from pymongo import MongoClient
from flask import request
from flask_login import UserMixin

class Temp(UserMixin):
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, u_id, name, password, level):
        self.id =u_id
        self.name = name
        self.password = password
        self.level = level

    def __repr__(self):
        return self.name

    def get_id(self):
        return self.id

    def is_admin(self):
        if self.level == 'C':
            return False

        if self.level == 'A' or 'B':
            return True

def encrypt_passowrd(password):
    return generate_password_hash(password)


def verify_password(user_password, password):
    return check_password_hash(user_password, password)

def str_to_dict(s):
    exec("c=" + s)
    return c

def query(tag, type):
    if type == 'id':
        user = MongoClient().safe_protocol.user.find_one({'_id':int(tag)})
    elif type == 'name':
        user = MongoClient().safe_protocol.user.find_one({'name':tag})
    else:
        return 'type error'
    return user

def delete_user(user):
    user_id = user.get('_id')
    MongoClient().safe_protocol.user.remove({'_id':int(user_id)})
    return json.dumps({"result":True}), 200

def login_u(current_user):
    user_id = current_user.id
    username = current_user.name
    level = current_user.level

    return json.dumps({"_id":user_id, "name":username, "level":level}), 200

def register_form():
    user_id = request.form['user_id']
    username = request.form['username']
    userpw = request.form['password']
    e_password = encrypt_passowrd(userpw)
    userlevel = request.form['level']

    return json.dumps({"_id":user_id, "name":username, "password":e_password, "level":userlevel})

def insert(new_user):
    try:
        MongoClient().safe_protocol.user.insert({'_id':int(new_user['_id']),'name':new_user['name'],'password':new_user['password'],'level':new_user['level']})
        return json.dumps({"result":True}),201
    except:
        return json.dumps([{'errorMsg': 'maybe id has error'},{'errorCode':'error_args'}]), 400

def update_set(user, new_set, flag):
    user_id = user.get('_id')

    if flag == 'pw':
        MongoClient().safe_protocol.user.update({'_id':int(user_id)},{'$set':{'password':encrypt_passowrd(new_set)}})
        return json.dumps({"result":True}), 202
    elif flag == 'level':
        MongoClient().safe_protocol.user.update({'_id':int(user_id)},{'$set':{'level':new_set}})
        return json.dumps({"result":True}), 202


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kw):
        tag = request.args.get('tag')
        user = query(tag, 'id')
        if user == None:
            return json.dumps([{'errorMsg': 'user is not exist'},{'errorCode':'uri_not_found'}]), 404

        if user.get('level') == 'C':
            return json.dumps([{'errorMsg': 'forbidden'},{'errorCode':'error_args'}]), 401
        return func(*args, **kw)

    return decorated_function
