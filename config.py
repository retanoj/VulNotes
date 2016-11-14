# coding:utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))

MAX_CONTENT_LENGTH = 5 * 1024 * 1024


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://vulnotes:vulnotes@127.0.0.1/vulnotes"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        @app.after_request
        def after_request(response):
            response.headers['Access-Control-Allow-Origin']  = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type, auth'
            response.headers['Access-Control-Expose-Headers']= 'auth'
            response.headers['Access-Control-Max-Age'] = 3600 * 24
            return response


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://vulnotes:vulnotes@127.0.0.1/vulnotes"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        @app.after_request
        def after_request(response):
            response.headers['Access-Control-Allow-Origin'] = 'http://me.me'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type, auth'
            response.headers['Access-Control-Expose-Headers']= 'auth'
            response.headers['Access-Control-Max-Age'] = 3600 * 24
            return response


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
