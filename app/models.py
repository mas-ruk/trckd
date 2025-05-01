# models.py

from app import db

class Card(db.Model):
    # sets the Scryfall card ID as the primary key
    card_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    
    ## SET INFORMATION
    
    # most sets have 3 character combinations but I couldn't find anywhere that could prove otherwise so I've put 5 for safety
    set_id = db.Column(db.String(5))
    collector_number = db.Column(db.String(16))
    rarity = db.Column(db.String(20)) # common, uncommmon, rare, mythic

    ## VISUALS
    image_url = db.Column(db.String(256))

    ## COLOURS
    mana_cost = db.Column(db.String(64))
    colours = db.Column(db.String(32)) # "W, U" 

    ## CARD ATTRIBUTE
    power = db.Column(db.String) # number or *
    toughness = db.Column(db.String)

