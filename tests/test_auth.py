from tests.test_setup import client
import logging


def signup(client, username, email, password):
    """{
            "username": "Remis",
            "email": "b@gmail.com",
            "password": "test1234"
        }
    """

    rv = client.post('/api/auth/signup', json={
        'username': username, 'email': email, 'password': password
    })

    # logging.getLogger().info("rv %s", rv)
    assert rv.status == '201 CREATED'
    return True


def login(client, username, email, password):
    """{ "username": "Remis",
         "email": "b@gmail.com",
         "password": "test1234"}"""

    payload = {'password': password}
    if username:
        payload['username'] = username
    elif email:
        payload['email'] = email

    rv = client.post('/api/auth/login', json=payload)
    assert rv.status == '200 OK'
    # logging.getLogger().info("rv %s", rv)
    json_login = rv.get_json()
    # logging.getLogger().info("json %s", json_login)
    return json_login['token']


def test_signup(client):
    '''Make sure signin is working and result token is returned.'''

    rv = signup(client, 'remis', 'b@mail.com', 'test1234')


def test_signup_login_username(client):
    '''Signup and login with username and password is working.'''

    assert signup(client, 'remis', 'b@mail.com', 'test1234')
    token = login(client, 'remis', '', 'test1234')
    assert token


def test_signup_login_email(client):
    '''Make sure signin and later login is working.'''

    assert signup(client, 'remis', 'b@mail.com', 'test1234')
    token = login(client, '', 'b@mail.com', 'test1234')
    assert token
