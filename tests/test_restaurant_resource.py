from tests.helpers import get_valid_token, token_headers, assert_success_200, assert_json_status
import json
from activity.model.entities import RestaurantModel, restaurant_schema


def test_restaurant_list(client):
    token = get_valid_token(client)
    response = client.get(
        "/api/v1/restaurant",
        headers=dict(Authorization="Bearer " + token),
        content_type="application/json",
    )
    assert_success_200(response)
    data = json.loads(response.data)
    assert data == []


def rest_restaurant_add(client, token: str, restaurant: RestaurantModel):
    restaurant_json = restaurant_schema.dump(restaurant)

    response = client.post(
        "/api/v1/restaurant",
        headers=token_headers(token),
        content_type="application/json",
        json=restaurant_json
    )
    assert_json_status(response, 201)
    data = json.loads(response.data)
    return data


def test_restaurant_add(client):
    token = get_valid_token(client)
    test_restaurant = RestaurantModel(name="restaurant 1", email="r1@mail.com")
    json = rest_restaurant_add(client, token, test_restaurant)
    assert json["name"] == "restaurant 1"
    assert json["email"] == "r1@mail.com"


def add_restaurant(client, name, email):
    token = get_valid_token(client)
    test_restaurant = RestaurantModel(name="restaurant 1", email="r1@mail.com")
    json = rest_restaurant_add(client, token, test_restaurant)

    # response = client.post(
    #     "/api/v1/restaurant",
    #     token_headers(token),
    #     content_type="application/json",
    #     json={"name": "restaurant 1",  "email": "r1@mail.com"}
    # )
    # assert_json_status(response, 201)
    # data = json.loads(response.data)

    rm = RestaurantModel(**json)
    return rm


def test_restaurant_update(client):
    token = get_valid_token(client)
    restaurant1 = add_restaurant(client, "restaurant 1", "mail@mail.com")
    response = client.put(
        f"/api/v1/restaurant/{restaurant1.id}",
        headers=token_headers(token),
        content_type="application/json",
        json={"name": "restaurant 1 - updated",
              "email": "updated_r1@mail.com"}
    )
    assert_json_status(response, 201)
    data = json.loads(response.data)
    assert data["name"] == "restaurant 1 - updated"
    assert data["email"] == "updated_r1@mail.com"


def test_restaurant_delete(client):
    token = get_valid_token(client)
    restaurant1 = add_restaurant(client, "restaurant 1", "mail@mail.com")
    restId = restaurant1.id
    response = client.delete(
        f"/api/v1/restaurant/{restaurant1.id}",
        headers=token_headers(token),
        content_type="application/json"
    )
    assert_json_status(response, 204)

    # following request for same restaurant should return 404
    url = f"/api/v1/restaurant/{restId}"
    response = client.get(
        url,
        headers=token_headers(token),
        content_type="application/json",
    )
    assert_json_status(response, 404)

    # count of stored restaurant should be 0

    response = client.get(
        "/api/v1/restaurant",
        headers=token_headers(token),
        content_type="application/json",
    )
    assert_success_200(response)
    data = json.loads(response.data)
    assert len(data) == 0
