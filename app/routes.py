from flask import render_template
from flask_login import login_required, current_user
from app import app
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
    user_cards = Card.query_filter_by(user_ID=current_user.userID).all()
    return render_template('visualize_data.html')



