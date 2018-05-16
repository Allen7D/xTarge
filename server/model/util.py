# !/usr/bin/env python
# _*_ coding: utf-8 _*_

# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from pymongo import MongoClient
from flask import request


class Utility(object):

    @staticmethod
    def get_data(table="cmnt", protocol_type=None):
        '''
            table: table (collection)
        '''
        limit = request.args.get("limit", 10, type=int)
        page = request.args.get("page", 1, type=int)
        _db = MongoClient().safe_protocol[table]
        # data = _db.find().sort("time", -1).skip(limit * (page - 1)).limit(limit)
        if table == "alert":
            alert_list = []
            alerts = _db.find().sort("time", -1).skip(limit * (page - 1)).limit(limit)
            for alert in alerts:
                alert = {
                    'time': alert.get('time'),
                    'protocol_type': alert.get('type'),
                    'message': alert.get('message')
                }
                alert_list.append(alert)

            if protocol_type:
                alert_list = list(
                    filter(lambda x: x['protocol_type'] == protocol_type, alert_list))
            return {'alerts': alert_list}

        elif table == "user":
            user_list = []
            users = _db.find().sort("register_time", -1).skip(limit * (page - 1)).limit(limit)
            for user in users:
                user_list.append({
                    'user_id': user.get('_id'),
                    'username': user.get('name'),
                    'level': user.get('level'),
                    'register_time': user.get('register_time')
                })

            return {'users': user_list}

        elif table == "os":
            op_list = []
            ops = _db.find().sort("time", -1).skip(limit * (page - 1)).limit(limit)
            for op in ops:
                op = {
                    'user_id': op.get('user_id'),
                    'username': op.get('user_name'),
                    'time': op.get('time'),
                    'protocol_type': op.get('protocol_type'),
                    'op': op.get('os')
                }
                op_list.append(op)
            return {'ops': op_list}

        elif table == "cmnt":
            cmnt_list = []
            cmnts = _db.find().sort("time", -1).skip(limit * (page - 1)).limit(limit)
            for cmnt in cmnts:
                cmnt = {
                    'time': cmnt.get('time'),
                    'buffer': cmnt.get('buffer'),
                    'ip': cmnt.get('ip')
                }
                cmnt_list.append(cmnt)

            return {'cmnts': cmnt_list}
