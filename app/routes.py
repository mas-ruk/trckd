from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/collection')
def collection():
    from app.models import Card
    return render_template('visualize_data.html')



