#coding:utf-8

import json

from datetime import datetime
from app import db, ma
from marshmallow import fields, validates, ValidationError, post_load, pre_load

class SuperEnum(object):
    def __init__(self, **kwargs):
        self.d = kwargs

    def __getattr__(self, item):
        return self.d.get(item, None)

    def get_enum_values(self):
        return tuple(self.d.values())

LevelType = SuperEnum(
    low     = 'low',
    medium  = 'medium',
    high    = 'high'
)

StatusType = SuperEnum(
    unresolved  = 'unresolved',
    resolved    = 'resolved'
)

class VulType(db.Model):
    __tablename__ = 'vul_types'
    id          = db.Column(db.Integer, primary_key=True)
    vul_type    = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, vul_type, *keys, **kwargs):
        self.vul_type = vul_type

    @staticmethod
    def data_init():
        db.session.add(VulType('SQL注入'))
        db.session.add(VulType('XSS'))
        db.session.add(VulType('命令执行'))
        db.session.add(VulType('代码执行'))
        db.session.add(VulType('任意文件操作'))
        db.session.add(VulType('逻辑漏洞'))
        db.session.add(VulType('信息泄露'))
        db.session.add(VulType('越权漏洞'))
        db.session.add(VulType('其他'))
        db.session.commit()

class VulRecord(db.Model):
    __tablename__ = 'vul_records'
    id              = db.Column(db.Integer, primary_key=True)
    vul_type_id     = db.Column(db.Integer, nullable=False)
    vul_name        = db.Column(db.String(1024), unique=False, nullable=False)
    vul_level       = db.Column(db.Enum(*LevelType.get_enum_values()), nullable=False)
    vul_status      = db.Column(db.Enum(*StatusType.get_enum_values()), default=StatusType.unresolved, nullable=False)
    vul_company     = db.Column(db.String(100), nullable=False)
    vul_detail      = db.Column(db.Text, nullable=True)
    vul_find_date   = db.Column(db.DateTime, default=datetime.now, nullable=False)
    vul_solve_date  = db.Column(db.DateTime, nullable=True)

    def from_dict(self, dic):
        if 'id' in dic:
            del dic['id']
        for k,v in dic.iteritems():
            setattr(self, k, v)

    @staticmethod
    def data_init():
        import random
        for i in xrange(30):
            db.session.add(VulRecord(vul_type_id=random.randint(1,7), vul_name="test"+str(i),
                                     vul_level=LevelType.low, vul_status=StatusType.unresolved,
                                     vul_company="company"+str(i)))
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class VulTypeSchema(ma.Schema):
    id          = fields.Integer()
    vul_type    = fields.String(required=True)

class VulRecordSchema(ma.Schema):
    id          = fields.Integer()
    vul_type_id = fields.Integer(required=True)
    vul_name    = fields.String(required=True)
    vul_level   = fields.String(required=True)
    vul_status  = fields.String(required=True)
    vul_company = fields.String(required=True)
    vul_detail  = fields.String(allow_none=True)
    vul_find_date  = fields.DateTime(required=True)
    vul_solve_date = fields.DateTime(allow_none=True)

    @validates('vul_level')
    def validate_vul_level(self, value):
        if value not in LevelType.get_enum_values():
            raise ValidationError('level must be in ' + str(LevelType.get_enum_values()))

    @validates('vul_status')
    def validate_vul_status(self, value):
        if value not in StatusType.get_enum_values():
            raise ValidationError('status must be in ' + str(StatusType.get_enum_values()))

    @validates('vul_type_id')
    def validate_vul_type_id(self, value):
        if not VulType.query.get(value):
            raise ValidationError('VulType is not exist')

    @post_load
    def make_object(self, data):
        vr = VulRecord()
        vr.from_dict(data)
        return vr
