from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    first_name = db.Column(db.String(150), unique=False)
    last_name = db.Column(db.String(150), unique=False)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email, first_name, last_name):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = f"{first_name} {last_name}"


class Posts(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=False, nullable=False)
    description = db.Column(db.Text)
    published = db.Column(db.Boolean, default=False)
    publisher = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"id={self.id}, title={self.title}, " \
               f"description={self.description},published={self.published}," \
               f" publisher={self.child}"
