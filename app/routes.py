from flask import render_template, request, jsonify
from app import app
import uuid

# Temporary in-memory "database"
shared_links = {}

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/share')
def share_page():
    return render_template('share.html')

@app.route('/generate_share_link', methods=['POST'])
def generate_share_link():
    data = request.get_json()
    selected_cards = data.get("cards", [])
    link_id = str(uuid.uuid4())[:8]
    shared_links[link_id] = selected_cards
    return jsonify({"link_id": link_id})

@app.route('/shared/<link_id>')
def view_shared_cards(link_id):
    cards = shared_links.get(link_id, [])
    return render_template('shared_cards.html', cards=cards)
