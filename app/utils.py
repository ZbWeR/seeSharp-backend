import os
import time
import uuid


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


def success(data, msg="success", code=0):
    return {"code": code, "msg": msg, "data": data}, 200


def fail(msg="fail", code=-1):
    return {"code": code, "msg": msg, "data": ""}, 200
