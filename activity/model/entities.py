from activity import db
from dataclasses import dataclass
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime
# from dataclasses_json import dataclass_json

from marshmallow import Schema, fields

RestaurantSchema = Schema.from_dict(
    {"id": fields.Int(),
     "name": fields.String(),
     "address": fields.String(),
     "email": fields.String()
     }
)

restaurant_schema = RestaurantSchema()


@dataclass
class ProjectModel(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Project ({self.id}: {self.name})>'


# @dataclasses_json
@dataclass
class VoteModel(db.Model):
    __tablename__ = 'vote'

    id: int
    user_id: int
    restaurant_id: int
    vote_rate: float
    voted_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, nullable=False)
    vote_rate = db.Column(db.Float, nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # def __init__(self, id: int, user_id: int, restaurant_id: int, vote_rate: float, voted_at: datetime):
    #     self.id = id
    #     self.user_id = user_id
    #     self.restaurant_id = restaurant_id
    #     self.vote_rate = vote_rate
    #     self.voted_at = voted_at

    @classmethod
    def get_today_votes(cls):
        return cls.query.filter_by(voted_at=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()


@dataclass
class RestaurantModel(db.Model):
    __tablename__ = 'restaurant'

    id: int
    name: str
    address: str
    email: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Restaurant id:{self.id} name:{self.name} >'

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

#     def __repr__(self):
#         return f'<User (name:{self.username} email:{self.email}>'


@dataclass
class UserModel(db.Model):
    __tablename__ = 'user'

    id: int
    username: str
    email: str
    password: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def hash_password(self, password: str):
        self.password = generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User username:{self.username} email:{self.email} password:"***">'
