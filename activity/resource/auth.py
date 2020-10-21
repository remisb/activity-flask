from flask import request, Response
from flask_restful import Resource, Api, reqparse
from activity.resource.errors import InternalServerError, UserWithEmailUsernameExist
from activity.model.entities import UserModel
from activity import db
import sqlalchemy
import datetime
from flask_jwt_extended import create_access_token


class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = UserModel(**body)
            # user.hash_password(user.password)
            user.save()

            # return Response({'id': str(user.id)}, response=201)
            return {'id': str(user.id)}, 201

        # except FieldDoesNotExist:
        #     raise SchemaValidationError
        # except NotUniqueError:
        #     raise EmailAlreadyExistsError
        except sqlalchemy.exc.IntegrityError:
            raise UserWithEmailUsernameExist

        except Exception as e:
            print(e)
            raise InternalServerError


class LoginApi(Resource):

    def post(self):
        try:
            body = request.get_json()
            username = body.get('username')
            user = None

            if username:
                # return {"a": "username 1"}
                user = UserModel.find_by_username(username)
                # user = User.objects.get(username=username)

            else:
                email = body.get('email')
                user = UserModel.find_by_email(email)

            if not user:
                return {"user": "username 3"}
                return {'error': 'Email or password invalid'}, 401

            authorized = user.check_password(body.get('password'))
            if not authorized:
                # return {"user": "username 4"}
                return {'error': 'Email or password invalid'}, 401

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(
                identity=str(user.id),
                expires_delta=expires)
            # return {"user": "username 5"}
            return {'token': access_token}

        # except (UnauthorizedError, DoesNotExist):
        #     raise UnauthorizedError
        except Exception as e:
            raise e
