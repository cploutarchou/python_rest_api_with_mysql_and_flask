from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    full_name = db.Column(db.String(220))

    def __repr__(self):
        return f"id={self.id}, username={self.username}, " \
               f"email={self.email},first_name={self.first_name}," \
               f" last_name={self.last_name}", \
               f"full_name={self.full_name}"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=False, nullable=False)
    description = db.Column(db.Text)
    published = db.Column(db.Boolean, default=False)
    publisher = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"id={self.id}, title={self.title}, " \
               f"description={self.description},published={self.published}," \
               f" publisher={self.publisher}"
