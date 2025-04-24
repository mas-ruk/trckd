from flask import render_template
from app import app

@app.route('/')
def index():
    return "This is text for testing!"

@app.route('/upload') 
def upload_data_view():
    return render_template('upload_data.html')