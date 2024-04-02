import base64
import json
import cv2
from flask import current_app, request
from flask_restful import Resource
import numpy as np
import requests
from app.utils import fail, success, check_uploaded_file


class ProductPrediction(Resource):

    def __init__(self):
        self.url = current_app.config['PRODUCT_RECOGNITION_URL']

    def get(self):
        return success("product prediction")

    def post(self):
        legal, file = check_uploaded_file(request, "image")
        if not legal:
            return fail(file, -1)

        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        _, buffer = cv2.imencode('.jpg', image)
        base64_string = base64.b64encode(buffer).decode('utf-8')
        data = {"key": ["image"], "value": [base64_string]}
        response = requests.post(self.url, data=json.dumps(data))
        print(response)
        return success(response.json())
