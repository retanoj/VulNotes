#coding:utf-8
import json
from flask import make_response


def errorRequest(msg=None, code=500):
    return make_response(json.dumps({'data': None, 'error': msg}), code)


def successRequest(msg=None, code=200):
    return make_response(json.dumps({'data': msg, 'error': None}), code)