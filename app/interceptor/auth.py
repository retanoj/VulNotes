# coding:utf-8
import jwt
import time
from functools import wraps
from flask import request
from ..utils import errorRequest, successRequest

SECRET_KEY = '1234qwer!@#$QWER'


def check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_code = request.headers.get('auth', None)
        if auth_code:
            de_auth_code = jwt.decode(auth_code, SECRET_KEY, algorithms=['HS256'])
            if de_auth_code.get('admin', False) == True:
                expire = de_auth_code.get('expire', 0)
                if int(time.time()) - expire > 3600 * 24 * 2:
                    return errorRequest('TOKEN-EXPIRED', 401)
                else:
                    return func(*args, **kwargs)

        return errorRequest('AUTH-ERROR', 401)

    return wrapper



