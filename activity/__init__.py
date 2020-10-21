from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from activity.config import config


# import pprint


db = SQLAlchemy()


def init_extensions(app):
    # db.init_app(app)
    # cors.init_app(app, resources={r"/*": {"origins": "*"}, })
    # jwt.init_app(app)
    # ma.init_app(app)

    jwt = JWTManager(app)
    db.init_app(app)
    api = Api(app)
    from activity.routes import register_routes

    register_routes(api, app)


def create_app(config_name='default', settings={}):
    """An application factory used to create new activity flask app."""

    print('=' * 80)
    print(f'CONFIG: {config_name}')
    print('-' * 80)

    # setupconfig

    app = Flask(__name__)

    a = config[config_name]
    app.config.from_object(a)
    app.config.from_mapping(settings)
    # app.config.update(settings)

    # print('Current app config:')
    # pprint.pprint(app.config)

    # jwt = JWTManager(app)
    # db.init_app(app)
    # api = Api(app)
    init_extensions(app)

    @app.route("/health")
    def health():
        return jsonify({"healty": True})

    @app.before_first_request
    def create_tables():
        db.drop_all()
        db.create_all()

    # init routes
    from activity.cmd import register_commands
    register_commands(app)
    return app

    # @app.cli.command("")
    # app.cli.add_command(create_database, name='create_database')
    # app.cli.add_command(init_db, name='init_db')
