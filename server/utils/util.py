#!/usr/bin/env python
# coding:utf-8

from flask import Response
import json
import os

def jsonify(data, status, mimetype):
  json_data = json.dumps(data)
  resp = Response(json_data, status=200, mimetype='application/json')
  return resp

def file_to_json(file):
  with open(file, 'r') as f:
    content = json.load(f)
  return content

def copy_file(src, dst):
    cmd = "cp " + src+ " " + dst
    os.system(cmd)

def convert(data):
    data = [s.split("-") for s in data.split("|")]
    return dict(data)
