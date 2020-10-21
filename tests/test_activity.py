
import pytest
from activity import create_app
from tests.test_setup import client

# from activity import activity


def test_config():
    """Test create_app without passing test config."""

    # assert create_app().testing
    assert create_app("testing", settings={
        "TESTING": True,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    }).testing


def test_health(client):
    response = client.get("/health")
    json_response = response.get_json()
    assert json_response["healty"]
