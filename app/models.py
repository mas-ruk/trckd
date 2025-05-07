from app import db

class User(db.Model):
    user_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

class Card(db.Model):
    card_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100))
    color = db.Column(db.String(50))
    rarity = db.Column(db.String(50))
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'))

    def __repr__(self):
        return f'<Card {self.name}>'


