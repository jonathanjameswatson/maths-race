from flask import Flask
import os

from mathsrace import db
from mathsrace.extensions import socketio
from mathsrace.commands import init_db_command
from mathsrace.blueprints.main import main
from mathsrace.blueprints.auth import auth
from mathsrace.blueprints.game import game


def create_app(config_param=None):
    app = Flask(__name__, instance_relative_config=True)

    if config_param is None:
        with app.app_context():
            from mathsrace import config
            config_file = config.base_config()
    else:
        config_file = config_param

    app.config.from_object(config_file)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    socketio.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(game)


def register_commands(app):
    for command in [init_db_command]:
        app.cli.command()(command)
