from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    user_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def get_id(self):
        return self.user_ID