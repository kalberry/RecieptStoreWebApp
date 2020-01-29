import os

class Config(object):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'mysecretkey'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    APP_DIR = os.path.abspath(os.path.join(BASE_DIR, 'app'))
    IMG_DIR = os.path.abspath(os.path.join(APP_DIR, 'itemImages'))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['kylealberry@gmail.com']
