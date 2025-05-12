from flask import render_template
from app import app, db
from app.models import Card

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
    cards = Card.query.limit(200).all()
    return render_template('visualize_data.html', cards=cards)
