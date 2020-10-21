import dataclasses
from flask import request, json
from flask_restful import Resource, Api, reqparse
from activity.model.entities import RestaurantModel
from activity import db
from activity.model.entities import restaurant_schema


class RestaurantListApi(Resource):
    def get(self):
        list = RestaurantModel.query.all()
        # return _schema.dump(list)
        return [restaurant_schema.dump(restaurant) for restaurant in list]

    def post(self):
        body = request.get_json()

        try:
            restaurant = RestaurantModel(**body)
            restaurant.save()

            return dataclasses.asdict(restaurant), 201

        except Exception as e:
            print(e)
            return e, 500


class RestaurantApi(Resource):
    def get(self, restaurant_id):
        return RestaurantModel.query.get_or_404(restaurant_id)
        # return RestaurantModel.get_or_404(restaurant_id)

    def put(self, restaurant_id):
        body = request.get_json()
        restaurant = RestaurantModel(**body)
        restaurant.save()
        return dataclasses.asdict(restaurant), 201

    def delete(self, restaurant_id):
        try:
            new_id = restaurant_id
            db.session.query(RestaurantModel).filter_by(id=new_id).delete()
            db.session.commit()
            return None, 204
        except Exception as e:
            return None, 500

    def delete_old(self, restaurant_id):
        rm = RestaurantModel.find_by_id(restaurant_id)
        if rm:
            rm.delete()

        return None, 204
