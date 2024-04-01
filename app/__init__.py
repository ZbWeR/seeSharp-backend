from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from config import Config
from .routes import HelloWorld, FaceAuth
from .Face import FaceManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 跨域
    CORS(app)
    # 初始化人脸识别模块
    FaceManager(app.config['KNOWN_FACES_DIR'])
    # 路由
    api = Api(app)
    api.add_resource(HelloWorld, '/hello')
    api.add_resource(FaceAuth, '/face-auth')

    return app
