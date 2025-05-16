import time
import requests
import json
from app import app, db
from app.models import Card
from flask_login import current_user

## USE THIS SCRIPT CAREFULLY IT WILL OVERRITE ALL YOUR ACQUISITION AND CURRENT PRICE COLUMNS TO TODAYS CONTENT
## AS FETCHED FROM THE SCRYFALL API

def migrate_price_data():
    """Migrate data from old price column to new acquisition_price and current_price columns"""
    with app.app_context():
        # Get all cards with price but missing acquisition_price
        cards = Card.query.filter(
            Card.price.isnot(None),
            (Card.acquisition_price.is_(None) | Card.current_price.is_(None))
        ).all()
        
        count = 0
        for card in cards:
            # Copy original price to both acquisition_price and current_price if they're empty
            if card.price:
                if not card.acquisition_price:
                    card.acquisition_price = card.price
                    count += 1
                if not card.current_price:
                    card.current_price = card.price
                    count += 1
        
        # Save changes
        db.session.commit()
        print(f"Updated {count} price values for {len(cards)} cards")

def update_card_prices():
    """Update card prices by querying Scryfall API"""
    with app.app_context():
        # Get all cards that need price updates
        cards = Card.query.all()
        
        total_cards = len(cards)
        updated_count = 0
        error_count = 0
        
        print(f"Starting price update for {total_cards} cards...")
        
        for index, card in enumerate(cards):
            try:
                # Skip cards without necessary identifiers
                if not card.set_code or not card.collector_number:
                    print(f"Skipping card '{card.name}' (missing set code or collector number)")
                    continue
                
                # Build Scryfall API URL
                api_url = f"https://api.scryfall.com/cards/{card.set_code}/{card.collector_number}"
                
                # Display progress
                print(f"[{index+1}/{total_cards}] Updating {card.name} ({card.set_code}/{card.collector_number})...")
                
                # Query Scryfall API
                response = requests.get(api_url)
                
                # Check if the request was successful
                if response.status_code == 200:
                    card_data = response.json()
                    
                    # Get price in USD if available
                    if 'prices' in card_data and 'usd' in card_data['prices'] and card_data['prices']['usd']:
                        # Update current price
                        card.current_price = card_data['prices']['usd']
                        
                        # Set acquisition price if it doesn't exist
                        if not card.acquisition_price:
                            card.acquisition_price = card_data['prices']['usd']
                        
                        # Store image URIs if they exist and aren't already stored
                        if 'image_uris' in card_data and not card.image_uris:
                            card.image_uris = json.dumps(card_data['image_uris'])
                        
                        updated_count += 1
                    else:
                        print(f"  No price data available for this card")
                else:
                    print(f"  Error: API returned status code {response.status_code}")
                    error_count += 1
                
                # Respect Scryfall rate limits (50-100ms delay between requests)
                time.sleep(0.1)
                
            except Exception as e:
                print(f"  Error updating card {card.name}: {str(e)}")
                error_count += 1
                time.sleep(0.5)  # Longer pause after an error
        
        # Save all changes
        db.session.commit()
        print(f"Update complete: {updated_count} cards updated, {error_count} errors")

if __name__ == "__main__":
    migrate_price_data()
    update_card_prices()