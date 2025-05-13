from app import db
from flask_login import UserMixin
import datetime

class User(UserMixin, db.Model):
    user_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def get_id(self):
        return self.user_ID
     
class Card(db.Model):
    card_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100))
    color = db.Column(db.String(50))
    rarity = db.Column(db.String(50))
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'))

    def __repr__(self):
        return f'<Card {self.name}>'

class SharedLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.String(8), unique=True, nullable=False)
    cards_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)