from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config.config import config_by_name
from .config.app_config import load_configurations, configure_logging

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    load_configurations(app)
    configure_logging()
    return app
