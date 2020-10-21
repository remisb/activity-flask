import dataclasses
import json
import datetime
import sys
from threading import RLock
from flask_restful import Resource, Api, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from activity.model.entities import VoteModel
from marshmallow import Schema, fields

mock_vote_rates = {}

VoteSchema = Schema.from_dict(
    {"id": fields.Int(),
     "user_id": fields.Int(),
     "restaurant_id": fields.Int(),
     "vote_rate": fields.Float(),
     "voted_at": fields.DateTime()
     }
)

_schema = VoteSchema()


lock = RLock()
vote_lock = RLock()


def get_vote_rate(user_id: int):
    mock_next_rate = {1.0: 0.5, 0.5: 0.25, 0.25: 0.25}

    lock.acquire()
    try:
        current_rate = mock_vote_rates.get(user_id, 1.0)
        print("mock_vote_rates", mock_vote_rates)
        print(f"current_rate 0: {current_rate}")
        sys.stdout.flush()
        mock_vote_rates[user_id] = mock_next_rate[current_rate]
        print(f"current_rate 1: {current_rate}")
        return current_rate
    finally:
        lock.release()


class VoteApi(Resource):
    @jwt_required
    def post(self, restaurant_id: int):
        vote_lock.acquire()

        body = request.get_json()
        current_user = get_jwt_identity()

        user_id = int(current_user)
        current_rate = get_vote_rate(user_id)
        print(f"current_rate: {current_rate}")
        vote = VoteModel(
            user_id=user_id, restaurant_id=restaurant_id, vote_rate=current_rate)
        vote.save()

        print(
            f'vote api rate:{current_rate} id:{vote.id} resturant_id:{vote.restaurant_id} user_id:{vote.user_id} vote_rate:{vote.vote_rate} vote_at:{vote.voted_at}')
        vote_lock.release()
        return _schema.dump(vote), 201


class VoteListApi(Resource):
    def get(self):
        list = VoteModel.query.all()
        return [_schema.dump(vote) for vote in list]
