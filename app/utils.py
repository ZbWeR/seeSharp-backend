import base64
import os
import time
import uuid

import cv2
import numpy as np


def generate_unique_id(name):
    """
    构造唯一的名称
    """
    base_name = os.path.basename(name)
    _, ext = os.path.splitext(base_name)
    unique_id = uuid.uuid4()
    short_id = str(unique_id).split('-')[0]
    timestamp = time.strftime('%H%M%S', time.localtime())
    return f'{timestamp}_{short_id}{ext}'


def singleton(cls):
    """
    单例装饰器。
    """
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    if '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_uploaded_file(request, key):
    if key not in request.files:
        return False, "No file part"
    file = request.files[key]
    if file.filename == '':
        return False, "No selected file"
    if not allowed_file(file.filename):
        return False, "Invalid file type"
    return True, file


def blob2base64(file_data):
    blob = np.frombuffer(file_data, np.uint8)
    image = cv2.imdecode(blob, cv2.IMREAD_COLOR)
    _, buffer = cv2.imencode('.jpg', image)
    base64_string = base64.b64encode(buffer).decode('utf-8')
    return base64_string


def success(data, msg="success", code=0):
    return {"code": code, "msg": msg, "data": data}, 200


def fail(msg="fail", code=-1):
    return {"code": code, "msg": msg, "data": ""}, 200
