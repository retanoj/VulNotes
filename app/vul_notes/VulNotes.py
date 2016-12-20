# coding:utf-8
import datetime
from flask_restful import Resource
from flask import request
from ..models import VulRecord, VulRecordSchema
from ..models import VulType, VulTypeSchema
from ..models import StatusType
from ..utils import errorRequest, successRequest
from ..interceptor import auth


class VulStatus(Resource):
    """
    漏洞状态
    """

    decorators = [auth.check]

    def put(self, id):
        """
        更改
        :param id: int
        :return: { "status": string (resolved/unresolved) }
        """
        postdata = request.get_json(force=True)
        vr = VulRecord.query.get_or_404(id)
        if not vr:
            return errorRequest("record is not exists")
        if postdata.get('status', None) not in StatusType.get_enum_values():
            return errorRequest("status is not right")

        vr.vul_status = postdata.get('status')
        if postdata.get('status') == 'resolved':
            vr.vul_solve_date = datetime.datetime.now()
        else:
            vr.vul_solve_date = None
        vr.update()
        return successRequest()


class VulNote(Resource):
    """
    对单个漏洞接口,通过id访问
    """

    decorators = [auth.check]

    def get(self, id):
        """
        获取漏洞记录
        :param id: int
        :return: {
          "id": int,
          "vul_company":    string,
          "vul_detail":     text,
          "vul_find_date":  string,
          "vul_level":      string,
          "vul_name":       string,
          "vul_solve_date": string,
          "vul_status":     string,
          "vul_type": {
            "id":       int,
            "vul_type": string
          }
        }
        """
        vr = VulRecord.query.get_or_404(id)
        vrs = VulRecordSchema()
        return successRequest(vrs.dump(vr).data)

    def put(self, id):
        """
        更新漏洞记录
        :param id: int
        :return: {
          "vul_company":    string,
          "vul_detail":     string,
          "vul_find_date":  string,
          "vul_level":      string(limit low, medium, high),
          "vul_name":       string,
          "vul_solve_date": string,
          "vul_status":     string(limit unresolved, resolved),
          "vul_type_id":    int
        }
        """
        new_vr = request.get_json(force=True)

        vrs = VulRecordSchema()
        errors = vrs.validate(new_vr)
        if errors:
            return errorRequest(errors)

        vr = VulRecord.query.get_or_404(id)
        vr.from_dict(new_vr)
        vr.update()
        return successRequest(vrs.dump(vr).data)

    def delete(self, id):
        """
        删除漏洞记录
        :param id: int
        :return:
        """
        vr = VulRecord.query.get_or_404(id)
        vr.delete()
        return successRequest()


class VulTypeList(Resource):

    decorators = [auth.check]

    def get(self):
        """
        获取漏洞类型列表
        :return: {
            "id": int,
            "vul_type": string
        }
        """
        vultypes = VulType.query.all()
        vtr = VulTypeSchema(many=True)
        return successRequest(vtr.dump(vultypes).data)


class VulNoteList(Resource):

    decorators = [auth.check]

    def get(self):
        """
        获取漏洞列表
        :return: {
          "id":             int,
          "vul_type_id":    int,
          "vul_name":       string,
          "vul_level":      string(limit low, medium, high),
          "vul_status":     string(limit resolved, unresolved),
          "vul_company":    string,
          "vul_detail":     string,
          "vul_find_date":  datetime,
          "vul_solve_date": datetime
        }
        """
        pageSize = int(request.args.get('pageSize', 20))  # default: 20 records
        pageNum = int(request.args.get('pageNum', 1)) - 1  # default: 1
        vulrecords = VulRecord.query \
            .order_by(VulRecord.id.desc()) \
            .limit(pageSize) \
            .offset(pageNum * pageSize) \
            .all()
        vrs = VulRecordSchema(many=True)
        resp = {"total_count":VulRecord.query.count(), "items":vrs.dump(vulrecords).data}
        return successRequest(resp)

    def post(self):
        """
        添加漏洞记录
        :return: {
          "vul_name":       string,
          "vul_company":    string,
          "vul_detail":     string,
          "vul_level":      string(limit low, medium, high),
          "vul_type_id":    int
        }
        """
        new_vr = request.get_json(force=True)
        if 'id' in new_vr:
            del new_vr['id']
        vrs = VulRecordSchema()
        vr, errors = vrs.load(new_vr)
        if errors:
            return errorRequest(errors)
        vr.insert()
        return successRequest(vrs.dump(vr).data)


class VulNoteBriefList(Resource):

    decorators = [auth.check]

    def get(self):
        """
        获取漏洞简要列表
        :return:
        """
        pageSize = int(request.args.get('pageSize', 20))  # default: 20 records
        pageNum = int(request.args.get('pageNum', 1)) - 1  # default: 1

        vulrecords = VulRecord.query \
            .with_entities(VulRecord.id, VulRecord.vul_name, VulRecord.vul_status,
                           VulRecord.vul_company, VulRecord.vul_find_date) \
            .order_by(VulRecord.id.desc())

        keyword = request.args.get('keyword', '')
        field = request.args.get('field', None)
        if field == 'company':
            vulrecords = vulrecords.filter(VulRecord.vul_company.like('%' + keyword + '%'))
        elif keyword != '':
            vulrecords = vulrecords.filter(VulRecord.vul_name.like('%' + keyword + '%'))
        total_count = vulrecords.count()

        vulrecords = vulrecords.limit(pageSize) \
            .offset(pageNum * pageSize) \
            .all()
        vrs = VulRecordSchema(many=True)
        resp = {"total_count":total_count, "items":vrs.dump(vulrecords).data}
        return successRequest(resp)