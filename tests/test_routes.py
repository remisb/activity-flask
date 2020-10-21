from flask import Flask, jsonify
from flask_restful import Resource, Api
from activity.routes import register_routes
from tests.helpers import get_valid_token, assert_success_200, assert_json_status
import json


def register_util_routes(app):
    @app.route("/health")
    def health():
        return jsonify("healthy")


def test_health():
    app = Flask(__name__)
    api = Api(app)
    register_routes(api, app)
    register_util_routes(app)
    client = app.test_client()
    url = '/health'

    response = client.get(url)
    json = response.get_json()
    # assert response.get_data() == b'healthy'
    assert response.status_code == 200
