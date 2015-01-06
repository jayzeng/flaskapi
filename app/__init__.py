from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(stage):
    app = Flask(__name__)
    config_inst = config[stage]
    app.config.from_object(config_inst)

    is_debug = True if hasattr(config_inst, 'DEBUG') else False
    app.debug = is_debug

    db.init_app(app)

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')

    return app
