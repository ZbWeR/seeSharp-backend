from flask_restful import Resource, reqparse
from flask import request

from app.utils import allowed_file, fail, success
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
        return success(data)


class FaceAuth(Resource):

    def get(self):
        known_faces = FaceManager().get_known_faces()
        return success(known_faces)

    def post(self):
        if 'image' not in request.files:
            return fail("No file part", -1)

        file = request.files['image']
        if file.filename == '':
            return fail("No selected file", -1)
        if not allowed_file(file.filename):
            return fail("Invalid file type", -1)

        file_name = file.filename
        file_blob = file.read()
        face_manager = FaceManager()
        res = face_manager.add_new_face(file_blob, file_name)
        if res:
            return success({"name": file_name})
        return fail("Failed to add face, Please Check the image", -1)
