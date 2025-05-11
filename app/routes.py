from flask import render_template
from app import app
import requests


@app.route('/')
def index():
    return render_template('homepage.html')

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
    response = requests.get('https://api.scryfall.com/cards/search?q=f%3Astandard&order=popularity&page=1')
    
    cards = []
    if response.status_code == 200:
        data = response.json()
        cards = data.get('data', [])

    return render_template('visualize_data.html', cards=cards)



