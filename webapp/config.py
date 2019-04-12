# coding: utf-8


class Config(object):
    pass


class DevConfig(Config):
    DEBUG = True
    JSON_AS_ASCII = False   # 解决 rest framework 中文乱码
    # SQLALCHEMY_DATABASE_URI = "sqlite:///../bitwar.db"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123123@192.168.0.202:6608/bitwar"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CSRF_ENABLED = True
    SECRET_KEY = '919e08e1a692e0130b0c0e600e5f09b7'


class ProdConfig(Config):
    pass


class TestConfig(Config):
    pass
