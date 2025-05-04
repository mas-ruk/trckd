# models.py
from app import db
from datetime import datetime

class User(db.Model):
    user_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False, unique=True)

class Card(db.Model):
    __tablename__ = 'cards'
    
    # Core fields
    id = db.Column(db.String(64), primary_key=True)  # Scryfall UUID
    name = db.Column(db.String(128), nullable=False)
    lang = db.Column(db.String(3), default='en')
    
    # Set info
    set_code = db.Column(db.String(5), nullable=False)  # e.g. 'MH2'
    set_name = db.Column(db.String(128))
    collector_number = db.Column(db.String(16))
    rarity = db.Column(db.String(20))  # common/uncommon/rare/mythic
    
    # Gameplay info
    mana_cost = db.Column(db.String(64))  # "{1}{U}{B}"
    cmc = db.Column(db.Float)
    type_line = db.Column(db.String(128))
    oracle_text = db.Column(db.Text)
    power = db.Column(db.String(8))  # Can be numbers or *
    toughness = db.Column(db.String(8))
    
    # Visuals
    image_uris = db.Column(db.JSON)  # Stores all image URLs as JSON
    color_identity = db.Column(db.JSON)  # ['W', 'U'], etc.
    
    # Timestamps
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Card {self.name} ({self.set_code})>'