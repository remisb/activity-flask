import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'convious-secret'
    JWT_TOKEN_LOCATION = ['headers']
    JWT_SECRET_KEY = 'convious-secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///activity.sqlite3'
    JWT_SECRET_KEY = 'convious-secret'


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    JWT_SECRET_KEY = 'covious4wnBg6nyHYKfmc2TpCOGI4nss'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///activity.sqlite3'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
