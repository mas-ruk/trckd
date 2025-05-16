from .extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    user_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    cards = db.relationship('Card', backref='user', lazy=True)

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
    price = db.Column(db.String(20))

    acquisition_price = db.Column(db.String(20))  # Price when added to collection
    current_price = db.Column(db.String(20))      # Current market price
    acquisition_date = db.Column(db.DateTime, default=db.func.current_timestamp())  # When it was added

    def __repr__(self):
        return f'<Card {self.name}>'

collection_card = db.Table(
    'collection_card',
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'), primary_key=True),
    db.Column('card_id',       db.Integer, db.ForeignKey('card.card_ID'),   primary_key=True)
)

class Collection(db.Model):
    __tablename__ = 'collection'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_ID     = db.Column(db.Integer, db.ForeignKey('user.user_ID'), nullable=False)

    # link into Card via the join table
    cards = db.relationship('Card', secondary=collection_card, backref='collections')

    def __repr__(self):
        return f'<Collection {self.name}>'
    
shared_link_card = db.Table(
  'shared_link_card',
  db.Column('link_id', db.String(36), db.ForeignKey('shared_link.link_id'), primary_key=True),
  db.Column('card_id', db.Integer,    db.ForeignKey('card.card_ID'),   primary_key=True),
)

class SharedLink(db.Model):
    __tablename__ = 'shared_link'
    link_id = db.Column(db.String(36), primary_key=True)  # UUID4 string
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'), nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())

    cards = db.relationship('Card', secondary=shared_link_card, backref='shared_links')

    def __repr__(self):
        return f'<SharedLink {self.link_id}>'