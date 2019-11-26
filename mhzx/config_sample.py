import os
from flask_uploads import IMAGES

DEBUG = True
IS_MOCK = True
MONGO_HOST = "39.97.250.47"


class Config:
    MONGO_URI = "mongodb://%s:27017/rtconfig" % MONGO_HOST
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PROT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'xiuqianli_2015@163.com'
    MAIL_PASSWORD = ''
    MAIL_DEBUG = True
    MAIL_SUBJECT_PREFIX = '[PyFly]-'
    WTF_CSRF_ENABLED = False
    UPLOADED_PHOTOS_ALLOW = IMAGES
    UPLOADED_PHOTOS_DEST = os.path.join(os.getcwd(), 'uploads')
    WHOOSH_PATH = os.path.join(os.getcwd(), 'whoosh_indexes')

    USE_CACHE = False
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = MONGO_HOST
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = ''
    CACHE_REDIS_DB = '0'


MONGO = {
    'hx': {
        'name': 'hx',
        'host': MONGO_HOST,
        'port': 27018
    }
}
