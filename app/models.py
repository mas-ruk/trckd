from app import db
from flask_login import UserMixin

# Association table for many-to-many between Collection and Card
collection_card = db.Table('collection_card',
    db.Column('collection_ID', db.Integer, db.ForeignKey('collection.collection_ID'), primary_key=True),
    db.Column('card_ID', db.Integer, db.ForeignKey('card.card_ID'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    user_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    cards = db.relationship('Card', backref='user', lazy=True)
    collections = db.relationship('Collection', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_ID)

    def __repr__(self):
        return f'<User {self.username}>'

class Card(db.Model):
    __tablename__ = 'card'

    card_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100))
    color = db.Column(db.String(50))
    rarity = db.Column(db.String(50))
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'), nullable=False)

    set_code = db.Column(db.String(50))
    set_name = db.Column(db.String(100))
    collector_number = db.Column(db.String(20))
    mana_cost = db.Column(db.String(50))
    cmc = db.Column(db.Float)
    type_line = db.Column(db.String(100))
    oracle_text = db.Column(db.String(255))
    power = db.Column(db.String(20))
    toughness = db.Column(db.String(20))

    image_uris = db.Column(db.Text)
    color_identity = db.Column(db.String(50))
    lang = db.Column(db.String(10))

    # Many-to-many relationship with Collection
    collections = db.relationship('Collection', secondary=collection_card, back_populates='cards')

    def __repr__(self):
        return f'<Card {self.name}>'

class Collection(db.Model):
    __tablename__ = 'collection'

    collection_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'), nullable=False)

    # Many-to-many relationship with Card
    cards = db.relationship('Card', secondary=collection_card, back_populates='collections')

    def __repr__(self):
        return f'<Collection {self.name} (User {self.user_ID})>'



