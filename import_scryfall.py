# import_scryfall.py
import requests
from app import app, db
from app.config import Config
from app.models import Card

def download_bulk_data():
    """Download Scryfall's bulk data"""
    print("Fetching bulk data...")
    bulk_data_url = "https://api.scryfall.com/bulk-data"
    response = requests.get(bulk_data_url)
    bulk_data = response.json()
    
    # Find the default cards dataset
    for item in bulk_data['data']:
        if item['type'] == 'default_cards':
            download_url = item['download_uri']
            break
    
    print("Downloading card data...")
    cards_data = requests.get(download_url).json()
    return cards_data

def import_cards_to_db(cards_data, limit=200):
    """Import cards to database with optional limit"""
    with app.app_context():
        print(f"Importing first {limit} cards...")
        for i, card_data in enumerate(cards_data[:limit]):
            # Skip digital-only cards and non-English cards for simplicity
            if (card_data['digital'] or 
                card_data['lang'] != 'en' or 
                'image_uris' not in card_data):
                continue
            
            # Check if card exists
            existing = db.session.get(Card, card_data['id'])
            if existing:
                continue
            
            # Prepare card data
            new_card = Card(
                id=card_data['id'],
                name=card_data['name'],
                set_code=card_data['set'],
                set_name=card_data['set_name'],
                collector_number=card_data['collector_number'],
                rarity=card_data['rarity'],
                mana_cost=card_data.get('mana_cost'),
                cmc=card_data['cmc'],
                type_line=card_data['type_line'],
                oracle_text=card_data.get('oracle_text', ''),
                power=card_data.get('power'),
                toughness=card_data.get('toughness'),
                image_uris=card_data['image_uris'],
                color_identity=card_data['color_identity'],
                lang=card_data['lang']
            )
            
            db.session.add(new_card)
            
            if i % 100 == 0:
                print(f"Processed {i} cards...")
                db.session.commit()
        
        db.session.commit()
        print("Import complete!")

if __name__ == '__main__':
    cards_data = download_bulk_data()
    import_cards_to_db(cards_data, limit=200)  # Start with 500 cards