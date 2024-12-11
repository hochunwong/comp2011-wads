from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    liveries = db.relationship('Livery')
    likes = db.relationship('Like', backref='user')


class Livery(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)

    img = db.Column(db.Text, nullable=True)

    author = db.relationship(lambda: User, uselist=False)
    likes = db.relationship('Like', backref='livery')
    

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    livery_id = db.Column(db.Integer, db.ForeignKey('livery.id'), nullable=False)
