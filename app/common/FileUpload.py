# coding:utf-8

import os
import time
import random
import string
from flask_restful import Resource
from flask import request, url_for, send_from_directory
from app.utils import errorRequest, successRequest
from config import basedir

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
file_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = basedir + '/static/uploads'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def gen_filename(filename):
    return str(int(time.time())) +''.join(random.sample(string.ascii_letters+string.digits, 5)) +'.' +filename.rsplit('.', 1)[1]


class FileUpload(Resource):
    def post(self, filename):
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = gen_filename(filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return successRequest(url_for('comm.fileupload', filename=filename))

        return errorRequest()

    def get(self, filename):
        return send_from_directory(UPLOAD_FOLDER, filename)
