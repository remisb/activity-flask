from werkzeug.exceptions import HTTPException


class UnauthorizedError(HTTPException):
    pass


class InternalServerError(HTTPException):
    pass


class UserWithEmailUsernameExist(HTTPException):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },

    "UserWithEmailUsernameExist": {
        "message": "User with such username or email already exist",
        "status": 500
    }
}
