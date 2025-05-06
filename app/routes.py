from flask import render_template, jsonify, request
from app import app
from app.models import Card

@app.route('/')
def index():
    return render_template('homepage.html')

<<<<<<< HEAD
@app.route('/collection')
def collection():
    return render_template('visualize_data.html')
=======
@app.route('/upload') 
def upload_data_view():
    return render_template('upload_data.html')

@app.route('/search')
def upload_search():
    return render_template('search.html')

@app.route('/upload_csv')
def upload_csv():
    return render_template('upload_csv.html')

@app.route('/collection')
def collection():
    return render_template('visualize_data.html')

# disabled in search only branch
# @app.route('/api/search_cards', methods=['GET'])
# def search_cards():
    """API endpoint to search cards by name"""
    # search_query = request.args.get('query', '')
    
    # If empty query, return all cards
    # if not search_query:
    #     cards = Card.query.limit(100).all()  # Limit to 100 to avoid huge responses
    # else:
        # Search by name using LIKE query (case-insensitive)
    #     cards = Card.query.filter(Card.name.ilike(f'%{search_query}%')).all()
    
    # Convert cards to JSON-serializable format
    # results = []
    # for card in cards:
    #     card_data = {
    #         'name': card.name,
    #         'image_uris': card.image_uris if hasattr(card, 'image_uris') else {},
    #         'oracle_text': card.oracle_text if hasattr(card, 'oracle_text') else '',
    #         'set_name': card.set_name if hasattr(card, 'set_name') else '',
    #         'set_code': card.set_code if hasattr(card, 'set_code') else '',
    #         'rarity': card.rarity if hasattr(card, 'rarity') else '',
    #         'mana_cost': card.mana_cost if hasattr(card, 'mana_cost') else '',
    #     }
    #     results.append(card_data)
    
    # return jsonify({'cards': results})
>>>>>>> feature/visualise-page
