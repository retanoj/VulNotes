#coding:utf-8

from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    from vul_notes import vn_bp
    app.register_blueprint(vn_bp, url_prefix='/vul')

    from common import comm
    app.register_blueprint(comm, url_prefix='/comm')

    return app
