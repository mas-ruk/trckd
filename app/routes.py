from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm
#import requests
import time

from .models import User, Card
from .extensions import db

main_bp = Blueprint('main', __name__)

# Landing page route - handles logging in and registering
@main_bp.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm(prefix='login')
    register_form = RegisterForm(prefix='register')
    resubmit = False

    # Change the active page depending if a form has just tried to be submitted incorrectly
    active_tab = 'home'
    if register_form.register_submit.data:
        active_tab = 'register'
    elif login_form.submit.data:
        active_tab = 'login'

    # Handle submission of registration form
    if register_form.register_submit.data and register_form.validate_on_submit():

        # Get values from registration form fields
        register_email = register_form.register_email.data
        username = register_form.username.data
        register_password = register_form.register_password.data
        register_remember = register_form.register_remember_me.data

        users = User.query.all()

        # Check if the entered email or username are already taken
        for user in users:
            if register_email == user.email:
                register_form.register_email.errors.append("Email already in use. Choose a different email.")
                resubmit = True

            if username == user.username:
                register_form.username.errors.append("Username already in use. Choose a different username.")
                resubmit = True

        # If the form doesn't have any errors, add the new user to the db, login the new user and load the logged-in home page
        if not resubmit:
            new_user = User(email=register_email, username=username, password=generate_password_hash(register_password))
            db.session.add(new_user)
            db.session.commit()
            if register_remember:
                login_user(new_user, remember=True)
            else:
                login_user(new_user)
            return redirect(url_for('main.home'))

    # Handle submission of login form
    elif login_form.submit.data and login_form.validate_on_submit():

        # Get values from login form fields
        login_email = login_form.login_email.data
        login_password = login_form.login_password.data
        login_remember = login_form.login_remember_me.data

        user = User.query.filter_by(email=login_email).first()

        # Check if the user exists/if their password is correct
        if user is None:
            login_form.login_email.errors.append("No user registered to that email address.")
            resubmit = True
        elif not check_password_hash(user.password, login_password):
            login_form.login_password.errors.append("Incorrect password.")
            resubmit = True

        # If the form doesn't have any errors, login the user and load the logged-in home page
        if not resubmit:
            if login_remember:
                login_user(user, remember=True)
            else:
                login_user(user)
            return redirect(url_for('main.home'))

    # Otherwise render the homepage again
    return render_template('homepage.html', login_form=login_form, register_form=register_form, active_tab=active_tab)

@main_bp.route('/upload') 
@login_required
def upload_data_view():
    return render_template('upload_data.html')

@main_bp.route('/search')
@login_required
def upload_search():
    return render_template('search.html')

@main_bp.route('/upload_csv')
@login_required
def upload_csv():
    return render_template('upload_csv.html')

@main_bp.route('/collection')
@login_required
def collection():
    # Get user's cards from database
    user_cards = Card.query.filter_by(user_ID=current_user.user_ID).all()
    
    # Convert stored data to template format
    cards_with_images = []
    for card in user_cards:
        try:
            # Convert stored image_uris string to dict if needed
            image_uris = {}
            if card.image_uris:
                import json
                try:
                    image_uris = json.loads(card.image_uris)
                except:
                    print(f"Error parsing image URIs for card {card.name}")

            card_data = {
                'name': card.name,
                'type_line': card.type_line or 'Unknown',
                'colors': card.color_identity.split(',') if card.color_identity else [],
                'rarity': card.rarity or 'common',
                'image_uris': image_uris
            }
            cards_with_images.append(card_data)
        except Exception as e:
            print(f"Error processing card {card.name}: {str(e)}")
            continue

    return render_template('visualize_data.html', cards=cards_with_images)

# Route for handling logout
@main_bp.route('/logout')
@login_required
def logout():
    # Logout user and return to the homepage
    logout_user()
    return redirect(url_for('main.index'))

@main_bp.route('/home')
@login_required
def home():
    # Load the homepage for logged-in users
    return render_template('logged_in_home.html')

