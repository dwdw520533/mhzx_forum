import mongoengine
from flask import Flask
from mhzx.controllers import config_blueprint
from .custom_functions import init_func
from mhzx.config import Config, MONGO
from mhzx.extensions import init_extensions
from mhzx.util import db_utils


for alias, attrs in MONGO.items():
    mongoengine.register_connection(alias, **attrs)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hx123'
    app.config.from_object(Config)
    init_extensions(app)
    init_func(app)
    config_blueprint(app)
    return app
