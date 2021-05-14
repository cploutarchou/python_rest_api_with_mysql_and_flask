from sqlalchemy import ForeignKey

from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=False, nullable=False)
    description = db.Column(db.Text)
    published = db.Column(db.Boolean, default=False)
    publisher = db.Column(db.Integer, ForeignKey(Users.id))

    def __repr__(self):
        return f"id={self.id}, title={self.title}, " \
               f"description={self.description},published={self.published}," \
               f" publisher={self.publisher}"
