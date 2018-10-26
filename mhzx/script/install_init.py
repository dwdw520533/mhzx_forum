from werkzeug.security import generate_password_hash
from datetime import datetime
import pymongo

client = pymongo.MongoClient(host="192.168.4.5", port=27017)
db = client["pysls"]


def init():
    options = [
        {
            'name': '网站标题',
            'code': 'title',
            'val': '时光诛仙'
        },
        {
            'name': '网站描述',
            'code': 'description',
            'val': '时光诛仙游戏论坛'
        },
        {
            'name': '网站关键字',
            'code': 'keywords',
            'val': '诛仙 私服 诛仙私服 时光诛仙 辰皇 破军'
        },
        {
            'name': '网站Logo',
            'code': 'logo',
            'val': '/static/images/logo.png'
        },
        {
            'name': '签到奖励区间（格式: 1-100）',
            'code': 'sign_interval',
            'val': '1-5'
        },
        {
            'name': '开启用户注册（0关闭，1开启)',
            'code': 'open_user',
            'val': '1'
        },
        {
            'name': '管理员邮箱(申请友链链接用到)',
            'code': 'email',
            'val': '569293863@qq.com'
        },
        {
            'name': '底部信息(支持html代码)',
            'code': 'footer',
            'val': 'Copyright © 2018 mhzx1345.com'
        },
    ]
    #db.options.insert_many(options)
    db.users.insert_one({
        'email': 'admin',
        'loginname': 'admin',
        'username': 'admin',
        'password': generate_password_hash('admin'),
        'is_admin': True,
        'renzheng': '超级管理员',
        'vip': 5,
        'coin': 99999,
        'avatar': '/static/images/avatar/1.jpg',
        'is_active': True,
        'create_at': datetime.utcnow(),
    })


if __name__ == '__main__':
    init()
