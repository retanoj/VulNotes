#coding:utf-8

from flask import Blueprint
from flask_restful import Api
from VulNotes import VulNote, VulNoteList, VulNoteBriefList
from VulNotes import VulCount, VulTypeList, VulStatus
from Auth import Login
from FileUpload import FileUpload

vn_bp = Blueprint('api', __name__)
api = Api(vn_bp)

api.add_resource(VulNoteList, '/vulnotelist')

api.add_resource(VulNoteBriefList, '/vulnotebrieflist')

api.add_resource(VulCount, '/vulcount')

api.add_resource(VulNote, '/vulnote/<int:id>')

api.add_resource(VulTypeList, '/vultypelist')

api.add_resource(VulStatus, '/vulstatus/<int:id>')

api.add_resource(FileUpload, '/uploads/<filename>')

api.add_resource(Login, '/login')