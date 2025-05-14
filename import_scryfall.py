# import_scryfall.py

import requests
import json
from app import app, db
from app.models import Card

def download_bulk_data():
    """Download Scryfall's bulk data."""
    print("Fetching bulk data metadata...")
    bulk_data_url = "https://api.scryfall.com/bulk-data"
    response = requests.get(bulk_data_url)
    response.raise_for_status()
    bulk_data = response.json()

    download_url = next((item['download_uri'] for item in bulk_data['data']
                         if item['type'] == 'default_cards'), None)
    
    if not download_url:
        raise ValueError("Could not find default_cards bulk data URI.")

    print("Downloading actual card data...")
    response = requests.get(download_url)
    response.raise_for_status()
    return response.json()


def import_cards_to_db(cards_data, limit=200):
    """Import card data into the database."""
    with app.app_context():
        print(f"Starting import of up to {limit} cards...")
        count = 0

        for card_data in cards_data:
            if count >= limit:
                break

        
            if card_data.get('digital') or card_data.get('lang') != 'en' or 'image_uris' not in card_data:
                continue

          
            new_card = Card(
                name=card_data['name'],
                type=card_data.get('type_line'),
                color=','.join(card_data.get('colors', [])),
                rarity=card_data.get('rarity'),
                user_ID=1,  
                set_code=card_data.get('set'),
                set_name=card_data.get('set_name'),
                collector_number=card_data.get('collector_number'),
                mana_cost=card_data.get('mana_cost'),
                cmc=card_data.get('cmc'),
                type_line=card_data.get('type_line'),
                oracle_text=card_data.get('oracle_text', ''),
                power=card_data.get('power'),
                toughness=card_data.get('toughness'),
                image_uris=json.dumps(card_data.get('image_uris')),  
                color_identity=','.join(card_data.get('color_identity', [])), 
                lang=card_data.get('lang')
            )

            db.session.add(new_card)
            count += 1

            if count % 50 == 0:
                print(f"Imported {count} cards so far...")
                db.session.commit()

        db.session.commit()
        print(f"Successfully imported {count} cards.")


if __name__ == '__main__':
    cards_data = download_bulk_data()
    import_cards_to_db(cards_data, limit=200)

