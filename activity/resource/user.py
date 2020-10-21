import dataclasses
from flask import request
from flask_restful import Resource
from activity.model.entities import UserModel


class UserListApi(Resource):
    def get(self):
        list = UserModel.query.all()
        return [dataclasses.asdict(user) for user in list]

    def post(self):
        body = request.get_json()

        try:
            user = UserModel(**body)
            user.save()

            return dataclasses.asdict(user), 201
        except Exception as e:
            print(e)
            return e, 500


class UserItemApi(Resource):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        return user

    def put(self, user_id):
        body = request.get_json()

        try:
            user = UserModel(**body)
            user.save()
            return dataclasses.asdict(user)

        except Exception as e:
            print(e)
            return e, 500
