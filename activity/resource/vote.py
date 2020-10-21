import dataclasses
import json
import datetime
import sys
import logging

from threading import Lock
from flask_restful import Resource, Api, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from activity.service.vote_rate import VoteRate

from activity.model.entities import VoteModel
from marshmallow import Schema, fields

VoteSchema = Schema.from_dict(
    {"id": fields.Int(),
     "user_id": fields.Int(),
     "restaurant_id": fields.Int(),
     "vote_rate": fields.Float(),
     "voted_at": fields.DateTime()
     }
)

_schema = VoteSchema()


vote_lock = Lock()


_vote_rate = VoteRate()

a = Lock()
call = 0
expected_rates = {1: 1.0, 2: 0.5, 3: 0.25, 4: 0.25}


def ss(user_id: int, restaurant_id: int):
    global call
    a.acquire()
    try:
        call = call + 1
        logging.getLogger().info(f'vote.py call: {call}')
        rate = _vote_rate.next_rate(user_id)

        logging.getLogger().info(
            f'vote.py vr: {rate} user_id:{user_id} call: {call}')

        vote = VoteModel(
            user_id=user_id, restaurant_id=restaurant_id, vote_rate=rate)
        vote.save()
        logging.getLogger().info(
            f'vote.py saved > VoteMode#  objId:{hex(id(vote))} id:{vote.id} vr: {rate} user_id:{user_id} call: {call}')

        return vote
        # vote = VoteModel(id=None,
        #                  user_id=user_id, restaurant_id=restaurant_id, vote_rate=rate, voted_at=None)
        # vote.save()
        # return vote
        return None
    finally:
        a.release()


class VoteApi(Resource):
    @jwt_required
    def post(self, restaurant_id: int):
        try:
            vote_lock.acquire()

            body = request.get_json()
            user_id = int(get_jwt_identity())
            vote = ss(user_id, restaurant_id)
            logging.getLogger().info(
                f'vote.py vote.objId: {hex(id(vote))} id:{vote.id} user:id:{vote.user_id} rate:{vote.vote_rate}')
            return _schema.dump(vote), 201
        finally:
            vote_lock.release()


class VoteListApi(Resource):
    def get(self):
        list = VoteModel.query.all()
        return [_schema.dump(vote) for vote in list]
