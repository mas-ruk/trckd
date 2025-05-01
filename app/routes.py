from flask import Flask, render_template, request
from app.forms import LoginForm, RegisterForm
from app import app

@app.route('/')
def index():
    login_form = LoginForm()
    register_form = RegisterForm()

    if login_form.validate_on_submit() and login_form.submit.data:
        email = login_form.email.data
        password = login_form.password.data
        # process data
    
    if register_form.validate_on_submit() and register_form.submit.data:
        email = register_form.email.data
        username = register_form.username.data
        password = register_form.password.data
        # process data

    return render_template('homepage.html', login_form=login_form, register_form=register_form)

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