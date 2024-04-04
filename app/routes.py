from flask_restful import Resource
from flask import current_app, request
import requests
import json

from app.utils import blob2base64, check_uploaded_file, fail, success
from .Face import FaceManager


class HelloWorld(Resource):
    """
    基础接口测试
    """

    def get(self):
        return success("hello")

    def post(self):
        data = request.json
        return success(data)


class FaceAuthController(Resource):
    """
    新增已知人脸信息
    """

    def get(self):
        known_faces = FaceManager().get_known_faces()
        return success(known_faces)

    def post(self):
        legal, file = check_uploaded_file(request, 'image')
        if not legal:
            return fail(file, -1)

        file_name = file.filename
        file_blob = file.read()
        face_manager = FaceManager()
        res = face_manager.add_new_face(file_blob, file_name)
        if res:
            return success({"name": file_name}, "Upload face success")
        return fail(
            "Failed to add face, Please Check if there is a face in the image", -1)


class FaceVerify(Resource):
    """
    人脸识别
    """

    def post(self):
        legal, file = check_uploaded_file(request, 'image')
        if not legal:
            return fail(file, -1)

        file_blob = file.read()
        res = FaceManager().recognize_face(file_blob)
        if res:
            return success(res, "Face verified")
        return fail("Face not verified", -1)


class ProductPrediction(Resource):

    def __init__(self):
        self.url = current_app.config['PRODUCT_RECOGNITION_URL']

    def get(self):
        return success("product prediction")

    def post(self):
        legal, file = check_uploaded_file(request, "image")
        if not legal:
            return fail(file, -1)

        base64_string = blob2base64(file.read())
        data = {"key": ["image"], "value": [base64_string]}
        try:
            response = requests.post(self.url, data=json.dumps(data))
            response.raise_for_status()
        except requests.RequestException as e:
            return fail(str(e), -1)

        try:
            res_data = response.json()
        except json.JSONDecodeError as e:
            return fail(str(e), -1)

        if 'value' in res_data and isinstance(res_data['value'], list) and len(
                res_data['value']) > 0:
            try:
                label_values = json.loads(res_data['value'][0].replace("'", '"'))
                return success(label_values)
            except json.JSONDecodeError as e:
                return fail(str(e), -1)
        return fail("Unknown error", -1)
