#!/usr/bin/env python
# coding:utf-8
import requests

def login():
	user_info = {'username': 'super_admin', 'password': 'super_admin'}
	r = requests.post("http://127.0.0.1:5000/login", data=user_info)
	print(r.text)

def logout():
	r = requests.get("http://127.0.0.1:5000/logout")
	print(r.text)

'''
http://127.0.0.1:5000/api/users
查看所有用户，没有限制，无参数传入，直接访问　‘localhost:5000/api/users’
'''
def all():
	r = requests.get("http://127.0.0.1:5000/api/users")
	print(r.text)


'''
新建用户，重置用户，删除用户，url中通过tag来传入操作者id;
post/put/delete中传入　被操作者信息，以及操作者的密码，即admin_password
'''
def register():
	user_info = {'user_id':000, 'username': 'test0', 'password': 'test0', 'level':'C','admin_password':'super_admin'}
	r = requests.post("http://127.0.0.1:5000/api/users?tag=111111", data=user_info)
	print(r.text)

def reset():
	user_info = {'user_id':000, 'new_level':'B', 'admin_password':'super_admin'}
	#user_info = {'user_id':000, 'new_password': 'test', 'admin_password':'super_admin'}
	r = requests.put("http://127.0.0.1:5000/api/users?tag=111111", data=user_info)
	print(r.text)

def delete():
	user_info = {'user_id':000, 'admin_password': 'super_admin'}
	r = requests.delete("http://127.0.0.1:5000/api/users?tag=111111", data=user_info)
	print(r.text)

def get_os_by_action_id():
	user_info = {'user_id':111111}
	f = requests.get("http://127.0.0.1:5000/api/action_id", data=user_info)
	print(r.text)

def get_os_by_action_time():
	user_info = {'s_time':'2017-01-11 14:32:38', 'e_time':'2017-01-12 14:32:39'}
	f = requests.get("http://127.0.0.1:5000/api/action_time", data=user_info)
	print(r.text)

def get_all_alert():
	r = requests.get("http://127.0.0.1:5000/api/alert")
	print(r.text)


login()
#logout()

#all()
#register()
#reset()
#delete()

#get_os_by_action_id()
#get_os_by_action_time()
#get_all_alert()

