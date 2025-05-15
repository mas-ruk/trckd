from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, login, db
from app.forms import LoginForm, RegisterForm
from app.models import User, Card, Collection, collection_card
import requests
import time
import json

@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm(prefix='login')
    register_form = RegisterForm(prefix='register')
    resubmit = False
    active_tab = 'home'

    if register_form.register_submit.data:
        active_tab = 'register'
    elif login_form.submit.data:
        active_tab = 'login'

    if register_form.register_submit.data and register_form.validate_on_submit():
        register_email = register_form.register_email.data
        username = register_form.username.data
        register_password = register_form.register_password.data
        register_remember = register_form.register_remember_me.data

        users = User.query.all()
        for user in users:
            if register_email == user.email:
                register_form.register_email.errors.append("Email already in use. Choose a different email.")
                resubmit = True
            if username == user.username:
                register_form.username.errors.append("Username already in use. Choose a different username.")
                resubmit = True

        if not resubmit:
            new_user = User(email=register_email, username=username, password=generate_password_hash(register_password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=register_remember)
            return redirect(url_for('home'))

    elif login_form.submit.data and login_form.validate_on_submit():
        login_email = login_form.login_email.data
        login_password = login_form.login_password.data
        login_remember = login_form.login_remember_me.data

        user = User.query.filter_by(email=login_email).first()
        if user is None:
            login_form.login_email.errors.append("No user registered to that email address.")
            resubmit = True
        elif not check_password_hash(user.password, login_password):
            login_form.login_password.errors.append("Incorrect password.")
            resubmit = True

        if not resubmit:
            login_user(user, remember=login_remember)
            return redirect(url_for('home'))

    return render_template('homepage.html', login_form=login_form, register_form=register_form, active_tab=active_tab)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    return render_template('logged_in_home.html')

@app.route('/upload')
@login_required
def upload_data_view():
    return render_template('upload_data.html')

@app.route('/search')
@login_required
def upload_search():
    return render_template('search.html')

@app.route('/upload_csv')
@login_required
def upload_csv():
    return render_template('upload_csv.html')

# Unified view for user's cards and collections
@app.route('/collection')
@login_required
def collection():
    user_cards = Card.query.filter_by(user_ID=current_user.user_ID).all()
    collections = Collection.query.filter_by(user_ID=current_user.user_ID).all()

    cards_with_images = []
    for card in user_cards:
        try:
            image_uris = json.loads(card.image_uris) if card.image_uris else {}
            card_data = {
                'id': card.card_ID,
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

    return render_template('visualize_data.html', cards=cards_with_images, collections=collections)

# View cards in a specific collection
@app.route('/collection/<int:collection_id>')
@login_required
def view_collection_cards(collection_id):
    collection = Collection.query.filter_by(collection_ID=collection_id, user_ID=current_user.user_ID).first_or_404()
    
    cards = []
    for card in collection.cards:
        try:
            image_uris = json.loads(card.image_uris) if card.image_uris else {}
            card_data = {
                'id': card.card_ID,
                'name': card.name,
                'type_line': card.type_line or 'Unknown',
                'colors': card.color_identity.split(',') if card.color_identity else [],
                'rarity': card.rarity or 'common',
                'image_uris': image_uris
            }
            cards.append(card_data)
        except Exception as e:
            print(f"Error parsing card in collection: {str(e)}")

    collections = Collection.query.filter_by(user_ID=current_user.user_ID).all()
    return render_template('visualize_data.html', cards=cards, collections=collections, active_collection=collection.name)

# Create new collection from form in visualize_data.html
@app.route('/create_collection', methods=['POST'])
@login_required
def create_collection():
    name = request.form.get('collection_name')
    if name:
        new_collection = Collection(name=name, user_ID=current_user.user_ID)
        db.session.add(new_collection)
        db.session.commit()
    return redirect(url_for('collection'))

# Add card to specific collection
@app.route('/collection/<int:collection_id>/add_card/<int:card_id>', methods=['POST'])
@login_required
def add_card_to_collection(collection_id, card_id):
    collection = Collection.query.filter_by(collection_ID=collection_id, user_ID=current_user.user_ID).first_or_404()
    card = Card.query.get_or_404(card_id)

    if card not in collection.cards:
        collection.cards.append(card)
        db.session.commit()

    return redirect(url_for('view_collection_cards', collection_id=collection.collection_ID))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))



