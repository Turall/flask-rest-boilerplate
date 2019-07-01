import sys
import os.path as op
import logging

from flask import jsonify
from connexion import FlaskApp
from connexion.resolver import RestyResolver
from flask.logging import default_handler

from core.extensions import db, ma, migrator


settings = {
    "development": "core.settings.DevelopmentConfig",
    "production": "core.settings.ProductionConfig",
    "testing": "core.settings.TestingConfig",
    "default": "core.settings.DevelopmentConfig",
}


class SettingsError(Exception):
    pass


class SwaggerError(Exception):
    pass


def get_config(setting_name):
    if settings.get(setting_name):
        return settings.get(setting_name)
    else:
        raise SettingsError("Given settings name does not exists: %s" % setting_name)


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    migrator.init_app(app)
    return None


def register_api(app):
    app.add_api('api.yaml',
                resolver=RestyResolver('app.controllers'))
    return None


def register_logger(app):
    log_formatter = logging.Formatter(
        "[%(asctime)s] - %(levelname)s - %(name)s - %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(log_formatter)
    if app.config["DEBUG"]:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)
    app.logger.removeHandler(default_handler)

    return None


def register_error_handlers(app):
    def create_error_handler(status_code, message):
        def error_handler(error):
            return jsonify(message=message), status_code

        return error_handler

    app.register_error_handlers(400, create_error_handler(400, "Bad request"))
    app.register_error_handlers(401, create_error_handler(401, "Unathorized"))
    app.register_error_handlers(403, create_error_handler(403, "Forbidden"))
    app.register_error_handlers(404, create_error_handler(404, "Not found"))


def create_app(config_name):
    config_obj = get_config(config_name)

    swagger_dir = op.abspath(op.join(op.dirname(__name__), 'api_specs'))

    cnnx_app = FlaskApp(__name__,
                        specification_dir=swagger_dir)
    flask_app = cnnx_app.app

    flask_app.config.from_object(config_obj)
    flask_app.app_context().push()

    register_logger(flask_app)
    register_extensions(flask_app)
    register_error_handlers(flask_app)
    register_api(cnnx_app)

    return flask_app
