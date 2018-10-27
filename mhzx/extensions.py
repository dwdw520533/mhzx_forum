from flask_mail import Mail
from flask_admin import Admin
from flask_admin.base import MenuView
from flask_login import LoginManager
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from mhzx.models import User
from mhzx.controllers import admin as admin_view
from flask_uploads import UploadSet, configure_uploads
from flask_oauthlib.client import OAuth
from mhzx.mongo import Product
# Whoosh相关
from mhzx.plugins import WhooshSearcher
from whoosh.fields import Schema, TEXT, ID, DATETIME
#from jieba.analyse import ChineseAnalyzer
from mhzx.util import cached
from mhzx.ops.user import user_sql
from mhzx.config import VIP_CREDIT

# 初始化Mail
mail = Mail()
# 初始化Flask-Admin
admin = Admin(name='后台管理')
mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'user.login'

# 图片上传
upload_photos = UploadSet('photos')

# Cache
# cache = Cache()

# OAuth
oauth = OAuth()
#oauth_weibo = oauth.remote_app('weibo', )

whoosh_searcher = WhooshSearcher()


def get_user_credit_balance(user):
    balance = user.get("credit", 0) - user.get("credit_used", 0)
    if balance < 0:
        mongo.db.users.update({"_id": user["_id"]}, {
            '$set': {"credit_used": user.get("credit", 0)}})
        balance = 0
    return balance


@cached(lambda x: "cache_refresh_user_data_%s" % str(x["_id"]), timeout=600)
def refresh_user_data(user):
    try:
        ret = user_sql.get_user_credit(user["game_user_id"])
        credit = ret.get("credit", 0) if ret else 0
        vip, user["credit"] = 0, credit
        credit_balance = get_user_credit_balance(user)
        user["credit_balance"] = credit_balance
        print("#refresh user:", user)
        for num, v in sorted(VIP_CREDIT, reverse=True):
            if credit < num:
                continue
            vip = v
            break
        mongo.db.users.update({"_id": user["_id"]}, {
            '$set': {"credit": credit, "vip": vip,
                     "credit_balance": credit_balance}})
    except KeyError:
        user["credit"] = 0
        user["credit_balance"] = 0


@login_manager.user_loader
def load_user(user_id):
    u = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not u:
        return None
    refresh_user_data(u)
    return User(u)


def init_extensions(app):
    whoosh_searcher.init_app(app)
    configure_uploads(app, upload_photos)
    mail.init_app(app)
    admin.init_app(app)
    mongo.init_app(app, "MONGO")
    oauth.init_app(app)
    login_manager.init_app(app)
    # if app.config.get('USE_CACHE', False):
    #     cache.init_app(app, {})

    with app.app_context():
        # 添加flask-admin视图
        admin.add_view(admin_view.UsersModelView(mongo.db['users'], '用户管理'))
        admin.add_view(admin_view.CatalogsModelView(mongo.db['catalogs'], '栏目管理'))
        admin.add_view(admin_view.PostsModelView(mongo.db['posts'], '帖子管理'))
        admin.add_view(admin_view.PassagewaysModelView(mongo.db['passageways'], '温馨通道'))
        admin.add_view(admin_view.FriendLinksModelView(mongo.db['friend_links'], '友链管理'))
        admin.add_view(admin_view.PagesModelView(mongo.db['pages'], '页面管理'))
        admin.add_view(admin_view.FooterLinksModelView(mongo.db['footer_links'], '底部链接'))
        admin.add_view(admin_view.AdsModelView(mongo.db['ads'], '广告管理'))
        admin.add_view(admin_view.OptionsModelView(mongo.db['options'], '系统设置'))
        admin.add_view(admin_view.ProductModelView(Product, name='商品管理'))

        # 初始化Whoosh索引
        # chinese_analyzer = ChineseAnalyzer()
        # post_schema = Schema(obj_id=ID(unique=True, stored=True), title=TEXT(stored=True, analyzer=chinese_analyzer)
        #                      , content=TEXT(stored=True, analyzer=chinese_analyzer), create_at=DATETIME(stored=True)
        #                      , catalog_id=ID(stored=True), user_id=ID(stored=True))
        # whoosh_searcher.add_index('posts', post_schema)


# def clear_cache(f):
#     @functools.wraps(f)
#     def decorator(*args, **kwargs):
#         cache.clear()
#         return f(*args, **kwargs)
#     return decorator

