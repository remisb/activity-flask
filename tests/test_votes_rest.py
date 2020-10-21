from tests.helpers import assert_success_200, assert_json_status, get_valid_token, token_headers, signup_user_get_token
from tests.test_restaurant_resource import test_restaurant_add
from functools import reduce

import json
import logging


def test_vote_list(client):
    token = get_valid_token(client)
    response = client.get(
        "/api/v1/vote",
        headers=token_headers(token),
        content_type="application/json",
    )
    assert_success_200(response)
    data = json.loads(response.data)
    assert not data


def _test_vote_add(client):
    token = get_valid_token(client)
    restaurant_id = 1
    th = token_headers(token)
    response = client.post(
        f"/api/v1/vote/{restaurant_id}",
        headers=token_headers(token)
    )
    assert_json_status(response, 201)
    data = json.loads(response.data)

    assert data["restaurant_id"] == restaurant_id
    assert data["user_id"] == 1
    assert data["vote_rate"] == 1


def palce_vote(client, token, restaurant_id: int):
    response = client.post(
        "/api/v1/vote",
        token_headers(token),
        content_type="application/json",
        json={"restaurant_id": 1}
    )


def _get_user_token(client, userNo: int):
    uname = f'user{userNo}'
    uemail = f'u{userNo}@mail.com'
    upass = f'pass{userNo}'
    token = signup_user_get_token(client, uname, uemail, upass)
    return token


def _get_restaurant(client, restaurantNo: int):
    rname = f'restaurant{restaurantNo}'
    test_restaurant_add(client)


def sum_total_vote_rates(votes):
    return reduce(
        (lambda t, vote: t + vote['vote_rate']), votes, 0.)


def _get_today_votes(client, token: str):
    today_votes = client.get(
        "/api/v1/vote",
        headers=token_headers(token)
    )
    assert_json_status(today_votes, 200)
    return json.loads(today_votes.data)


def _place_vote(client, restaurant_id: int, user_token: str):
    response = client.post(
        f'/api/v1/vote/{restaurant_id}',
        headers=token_headers(user_token)
    )
    assert_json_status(response, 201)
    result = json.loads(response.data)
    return result


def test_vote_today(client):

    # create test user tokens
    u1_token = _get_user_token(client, 1)
    u2_token = _get_user_token(client, 2)
    u3_token = _get_user_token(client, 3)

    # create test restaurants
    r1 = _get_restaurant(client, 1)

    _place_vote(client, 1, u1_token)
    _place_vote(client, 1, u1_token)
    _place_vote(client, 1, u1_token)
    _place_vote(client, 1, u1_token)

    today_votes = _get_today_votes(client, u1_token)
    assert len(today_votes) == 4
    assert sum_total_vote_rates(today_votes) == 2.0

    _place_vote(client, 1, u2_token)
    _place_vote(client, 1, u2_token)

    today_votes = _get_today_votes(client, u1_token)
    assert len(today_votes) == 6
    assert sum_total_vote_rates(today_votes) == 3.5


def assert_vote(actual_vote, restaurant_id, user_id, vote_rate):
    assert actual_vote['restaurant_id'] == restaurant_id
    assert actual_vote['user_id'] == user_id
    assert actual_vote['vote_rate'] == vote_rate
