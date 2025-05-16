import time
import requests
import json
import random
from datetime import datetime, timedelta
from app import app, db
from app.models import Card

def simulate_historical_prices():
    """
    Query Scryfall API for current prices, then simulate acquisition prices
    from a week ago by applying realistic market variations
    """
    with app.app_context():
        cards = Card.query.all()
        
        total_cards = len(cards)
        updated_count = 0
        
        print(f"Simulating historical prices for {total_cards} cards...")
        
        # Create a "week ago" timestamp for the acquisition date
        week_ago = datetime.now() - timedelta(days=7)
        
        for index, card in enumerate(cards):
            try:
                # Skip cards without necessary identifiers
                if not card.set_code or not card.collector_number:
                    print(f"Skipping card '{card.name}' (missing set code or collector number)")
                    continue
                
                # Build Scryfall API URL
                api_url = f"https://api.scryfall.com/cards/{card.set_code}/{card.collector_number}"
                
                # Display progress
                print(f"[{index+1}/{total_cards}] Processing {card.name}...")
                
                # Query Scryfall API
                response = requests.get(api_url)
                
                if response.status_code == 200:
                    card_data = response.json()
                    
                    # Get price in USD if available
                    if 'prices' in card_data and 'usd' in card_data['prices'] and card_data['prices']['usd']:
                        current_price = float(card_data['prices']['usd'])
                        card.current_price = str(current_price)
                        
                        # Simulate a historical price (with realistic market variation)
                        # Cards randomly fluctuate between -15% and +10% over a week
                        variation = random.uniform(-0.15, 0.10)
                        historical_price = current_price / (1 + variation)
                        card.acquisition_price = f"{historical_price:.2f}"
                        
                        # Set acquisition date to a week ago
                        card.acquisition_date = week_ago
                        
                        # Store image URIs if they don't exist
                        if 'image_uris' in card_data and not card.image_uris:
                            card.image_uris = json.dumps(card_data['image_uris'])
                        
                        updated_count += 1
                    else:
                        print(f"  No price data available for this card")
                else:
                    print(f"  Error: API returned status code {response.status_code}")
                
                # Respect Scryfall rate limits
                time.sleep(0.1)
                
            except Exception as e:
                print(f"  Error processing card {card.name}: {str(e)}")
                time.sleep(0.5)
        
        # Save all changes
        db.session.commit()
        print(f"Simulation complete: {updated_count} cards updated with historical price data")

if __name__ == "__main__":
    simulate_historical_prices()