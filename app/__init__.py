from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import Config
from .routes import HelloWorld, FaceAuth, FaceVerify
from .Face import FaceManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化人脸识别模块
    FaceManager(app.config['KNOWN_FACES_DIR'])
    # 跨域
    CORS(app)
    # JWT 与 路由
    JWTManager(app)
    api = Api(app)
    api.add_resource(HelloWorld, '/hello')
    api.add_resource(FaceAuth, '/face-auth')
    api.add_resource(FaceVerify, '/auth')

    return app
