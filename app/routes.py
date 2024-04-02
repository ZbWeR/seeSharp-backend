from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required
from flask import request

from app.utils import check_uploaded_file, fail, success
from .Face import FaceManager


class HelloWorld(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args')
        self.parser = parser

    def get(self):
        args = self.parser.parse_args()
        name = args['name']
        return success(f'Hello, {name}!')

    def post(self):
        data = request.json
        if 'name' not in data:
            return fail("Name is required", -1)
        access_token = create_access_token(identity=data['name'])
        return success({"access_token": access_token, "name": data['name']})


class FaceAuth(Resource):

    @jwt_required()
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

    def post(self):
        legal, file = check_uploaded_file(request, 'image')
        if not legal:
            return fail(file, -1)

        file_blob = file.read()
        res = FaceManager().recognize_face(file_blob)
        if res:
            return success(res, "Face verified")
        return fail("Face not verified", -1)
