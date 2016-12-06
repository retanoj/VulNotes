#coding:utf-8

from flask import Blueprint
from flask_restful import Api

from VulNotes import VulTypeList, VulStatus,VulNote, VulNoteList, VulNoteBriefList

vn_bp = Blueprint('vul', __name__)
api = Api(vn_bp)

api.add_resource(VulNoteList, '/vulnotelist')

api.add_resource(VulNoteBriefList, '/vulnotebrieflist')

api.add_resource(VulNote, '/vulnote/<int:id>')

api.add_resource(VulTypeList, '/vultypelist')

api.add_resource(VulStatus, '/vulstatus/<int:id>')
