# coding:utf-8

import jwt
import time
from flask_restful import Resource
from app.utils import successRequest
from app.interceptor.auth import SECRET_KEY


class Login(Resource):

    def get(self):
        """
        设置http头的auth字段
        :return:
        """
        auth_code = jwt.encode({'admin': True, 'expire': int(time.time())}, SECRET_KEY, algorithm='HS256')
        resp = successRequest()
        resp.headers.extend({'auth': auth_code})
        return resp