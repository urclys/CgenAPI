
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from flask_wtf import CSRFProtect


from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
import app

mail = Mail()
cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
csrf = CSRFProtect()


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    # csrf.init_app(app)
    jwt.init_app(app)


def register_blueprints(app):
    for module_name in ['base']:
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    # build dummy database on first request
    # @app.before_first_request
    # def initialize_database():
    #     db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def configure_logs(app):
    # soft logging
    try:
        basicConfig(filename='error.log', level=DEBUG)
        logger = getLogger()
        logger.addHandler(StreamHandler())
    except:
        pass


def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    register_extensions(app)
    configure_database(app)
    configure_logs(app)

    with app.app_context():
        register_blueprints(app)

    return app
