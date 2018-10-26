import os
from flask_uploads import IMAGES

DEBUG = True
IS_MOCK = True


if DEBUG:
    SQL_HOST = "127.0.0.1"
    MONGO_URI = "mongodb://127.0.0.1:27017/mhzx"
else:
    SQL_HOST = "172.31.187.199"
    MONGO_URI = "mongodb://127.0.0.1:27017/mhzx"


class Config:
    MONGO_URI = MONGO_URI
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
    CACHE_REDIS_HOST = '192.168.4.254'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = ''
    CACHE_REDIS_DB = '0'


SQL_CONF = {
    "host": SQL_HOST,
    "port": 1989,
    "user": "sa",
    "password": "123456",
    "database": "wm",
    "timeout": 10,
    "login_timeout": 5,
    "charset": "utf8"
}


ALIYUN_ACCESS_ID = "LTAIYfxArveaM9C6"
ALIYUN_ACCESS_SECRET = "cXg0iumlpoANhyKoPHyf23YqHdgjY0"

MONGO = {
    'mhzx': {
        'name': 'mhzx',
        'host': '127.0.0.1',
        'port': 27017,
    }
}
