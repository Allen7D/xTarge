from pymongo import MongoClient
from werkzeug.security import generate_password_hash

MongoClient().safe_protocol.user.drop()

user_id1 = 111111
username1 = 'super_admin'
password1 = 'super_admin'
e_password1 = generate_password_hash(password1)
level1 = 'A'

user_id2 = 222222
username2 = 'admin'
password2 = 'admin'
e_password2 = generate_password_hash(password2)
level2 = 'B'

user_id3 = 333333
username3 = 'gushenxing'
password3 = 'gushenxing'
e_password3 = generate_password_hash(password3)
level3 = 'C'

user_id4 = 12345
username4 = 'test'
password4 = 'test'
e_password4 = generate_password_hash(password3)
level4 = 'C'

MongoClient().safe_protocol.user.insert({'_id':user_id1,'name':username1,'password':e_password1,'level':level1})

MongoClient().safe_protocol.user.insert({'_id':user_id2,'name':username2,'password':e_password2,'level':level2})

MongoClient().safe_protocol.user.insert({'_id':user_id3,'name':username3,'password':e_password3,'level':level3})

MongoClient().safe_protocol.user.insert({'_id':user_id4,'name':username4,'password':e_password4,'level':level4})