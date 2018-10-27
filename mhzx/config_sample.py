import os
from flask_uploads import IMAGES

DEBUG = True
IS_MOCK = True


if DEBUG:
    SQL_HOST = "127.0.0.1"
    MONGO_HOST = "127.0.0.1"
else:
    SQL_HOST = "172.31.187.199"
    MONGO_HOST = "127.0.0.1"


class Config:
    MONGO_URI = "mongodb://%s:27017/mhzx" % MONGO_HOST
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
        'host': MONGO_HOST,
        'port': 27017
    }
}

ZONE_SSH = {
    "1": {
        "name": "征战天下",
        "code": "1",
        "host": SQL_HOST,
        "port": 22,
        "user": "root",
        "password": "123456"
    }
}

GAME_EMAIL_SERVER = (SQL_HOST, 29100)
