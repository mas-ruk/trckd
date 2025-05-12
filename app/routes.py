import requests
from app import db
from app.models import Card  

def fetch_and_store_scryfall_cards():
    url = 'https://api.scryfall.com/cards/search?q=f%3Astandard&order=popularity&page=1'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        cards_data = data.get('data', [])
        
        # Loop through each card and store it in the database
        for card_data in cards_data:
            # Check if the card already exists to avoid duplicates
            existing_card = Card.query.filter_by(name=card_data['name']).first()
            if not existing_card:
                # Create a new Card object and set its fields
                new_card = Card(
                    name=card_data.get('name'),
                    type=card_data.get('type_line'),
                    color=card_data.get('color_identity', ''),
                    rarity=card_data.get('rarity'),
                    set_code=card_data.get('set'),
                    set_name=card_data.get('set_name'),
                    collector_number=card_data.get('collector_number'),
                    mana_cost=card_data.get('mana_cost'),
                    cmc=card_data.get('cmc'),
                    type_line=card_data.get('type_line'),
                    oracle_text=card_data.get('oracle_text'),
                    power=card_data.get('power'),
                    toughness=card_data.get('toughness'),
                    image_uris=card_data.get('image_uris', {}).get('normal', ''),
                    color_identity=card_data.get('color_identity', ''),
                    lang=card_data.get('lang', 'en')
                )

                # Add the new card to the session and commit to save it
                db.session.add(new_card)
        
        # Commit the session to save all the new cards
        db.session.commit()
        print(f'{len(cards_data)} cards were added to the database.')

    else:
        print('Error fetching data from Scryfall.')

