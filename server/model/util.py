# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from pymongo import MongoClient
from flask import request

class Utility(object):
    @staticmethod
    def get_data(table="cmnt"):
        '''
            table: table (collection)
        '''
        limit = request.args.get("limit", 10, type=int)
        page = request.args.get("page", 1, type=int)
        _db = MongoClient().safe_protocol[table]
        # data = _db.find().sort("time", -1).skip(limit * (page - 1)).limit(limit)
        if table == "alert":
            data_list = []
            alerts = _db.find().sort("time", -1).skip(limit * (page - 1)).limit(limit)
            total = _db.count()
            for alert in alerts:
                alert = {
                    'time': alert.get('time'),
                    'protocol_type': alert.get('type'),
                    'message': alert.get('message')
                }
                data_list.append(alert)

            protocol_type = request.args.get("type")
            if protocol_type:
                data_list = list(filter(lambda x: x['protocol_type'] == protocol_type, data_list))
                total = len(data_list)
            return {'data': data_list, 'total': total}

        elif table == "user":
            data_list = []
            users = _db.find().sort("create_time", -1).skip(limit * (page - 1)).limit(limit)
            total = _db.count()
            for user in users:
                data_list.append({
                    'user_id': user.get('_id'),
                    'username': user.get('name'),
                    'level': user.get('level'),
                    'create_time': user.get('create_time')
                })

            return {'data': data_list, 'total': total}

        elif table == "oper":
            data_list = []
            opers = _db.find().sort("time", -1).skip(limit * (page - 1)).limit(limit)
            total = _db.count()
            for oper in opers:
                oper = {
                    'user_id': oper.get('user_id'),
                    'username': oper.get('user_name'),
                    'time': oper.get('time'),
                    'protocol_type': oper.get('protocol_type'),
                    'oper': oper.get('oper')
                }
                data_list.append(oper)
            return {'data': data_list, 'total': total}

        elif table == "cmnt":
            data_list = []
            cmnts = _db.find().sort("time", -1).skip(limit * (page - 1)).limit(limit)
            total = _db.count()
            for cmnt in cmnts:
                cmnt = {
                    'time': cmnt.get('time'),
                    'buffer': cmnt.get('buffer'),
                    'ip': cmnt.get('ip')
                }
                data_list.append(cmnt)
            return {'data': data_list, 'total': total}
