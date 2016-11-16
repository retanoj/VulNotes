#coding:utf-8

from flask import Blueprint
from flask_restful import Api

from Login import Login
from FileUpload import FileUpload

comm = Blueprint('comm', __name__)
api = Api(comm)

api.add_resource(FileUpload, '/uploads/<filename>')

api.add_resource(Login, '/login')