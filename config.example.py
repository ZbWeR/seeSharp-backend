# 请将此文件重命名为 config.py
class Config:
    PORT = 9697  # 服务端口
    HOST = '0.0.0.0'  # 服务主机
    PROPAGATE_EXCEPTIONS = True  # 异常传递

    # 人脸识别配置, 已知人脸目录
    KNOWN_FACES_DIR = './assets/known'
    # 商品识别模块配置, 商品识别接口地址
    PRODUCT_RECOGNITION_URL = 'http://xxx/xxx'
