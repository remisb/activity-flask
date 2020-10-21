import json
import logging


def signup_user(client, username, email, password):
    data = dict()
    if username:
        data["username"] = username
    if email:
        data["email"] = email
    if password:
        data["password"] = password

    return client.post(
        "/api/auth/signup", content_type="application/json", data=json.dumps(data)
    )


def login_user(client, username, email, password):
    data = dict()
    if username:
        data["username"] = username
    elif email:
        data["email"] = email

    if password:
        data["password"] = password

    return client.post(
        "/api/auth/login", content_type="application/json", data=json.dumps(data)
    )


def token_headers(token):
    return dict(Authorization="Bearer " + token)


def signup_user_get_token(client, username, email, password):
    signup_user(client,  username, email, password)
    response = login_user(client, username, email, password)
    data = json.loads(response.data)
    # logging.getLogger().info("data %s", data)
    return data["token"]


def get_valid_token(client):
    username = "usrname1"
    email = "usrname1@example.com"
    password = "Password1"
    signup_user(client, username, email, password)
    response = login_user(client, username, email, password)
    data = json.loads(response.data)
    return data["token"]


def assert_success_200(response):
    assert_json_status(response, 200)


def assert_json_status(response, status_code):
    assert response.status_code == status_code
    assert response.content_type == "application/json"
