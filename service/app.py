"""Below are all the imports for this file."""
import logging
from flask import Flask, Blueprint
from flask_restx import Api
from service.config import config_by_name
from service.v1.test import api as ns1
from service.v1.user_views import api as ns2
from .middleware import Middleware
from .custom_log import get_custom_formatter
from .models import db
from .custom_exceptions import errors

ROOT_URL = '/myservice'
api = Api(
    title='My Service',
    version='2.0',
    description='service Details', doc='/swagger/document'
)


def create_app(config_name):

    config = config_by_name[config_name]
    app = Flask(__name__)

    app.config.from_object(config)

    app.config["APPLICATION_ROOT"] = ROOT_URL
    db.init_app(app)

    api.add_namespace(ns1, path=ROOT_URL)
    api.add_namespace(ns2, path=ROOT_URL)

    api.init_app(app)

    # set custom log format\
    formatter = get_custom_formatter(config)
    app.logger.handlers[0].setFormatter(formatter)

    app.wsgi_app = Middleware(app.wsgi_app)
    app.register_blueprint(errors)

    return app
