from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, login, db
from app.forms import LoginForm, RegisterForm
from app.models import User, Card, Collection, CollectionCard
import requests
import time

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
            if register_remember:
                login_user(new_user, remember=True)
            else:
                login_user(new_user)
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
            if login_remember:
                login_user(user, remember=True)
            else:
                login_user(user)
            return redirect(url_for('home'))

    return render_template('homepage.html', login_form=login_form, register_form=register_form, active_tab=active_tab)


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


@app.route('/collection')
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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/home')
@login_required
def home():
    return render_template('logged_in_home.html')

# to create collections
@app.route('/collections/create', methods=['GET', 'POST'])
@login_required
def create_collection():
    if request.method == 'POST':
        collection_name = request.form.get('collection_name')
        if collection_name:
            new_collection = Collection(name=collection_name, user_ID=current_user.user_ID)
            db.session.add(new_collection)
            db.session.commit()
            return redirect(url_for('view_collections'))
    return render_template('create_collection.html')

#to view all collections for the current user:
@app.route('/collections')
@login_required
def view_collections():
    user_collections = Collection.query.filter_by(user_ID=current_user.user_ID).all()
    return render_template('collections.html', collections=user_collections)

#to view cards inside a specific collection:
@app.route('/collections/<int:collection_id>')
@login_required
def view_collection_cards(collection_id):
    collection = Collection.query.filter_by(collection_ID=collection_id, user_ID=current_user.user_ID).first_or_404()
    collection_cards = CollectionCard.query.filter_by(collection_ID=collection.collection_ID).all()
    
    cards = []
    for cc in collection_cards:
        card = Card.query.get(cc.card_ID)
        if card:
            cards.append(card)
    
    return render_template('collection_cards.html', collection=collection, cards=cards)

#to add a card to a collection:
@app.route('/collections/<int:collection_id>/add_card/<int:card_id>', methods=['POST'])
@login_required
def add_card_to_collection(collection_id, card_id):
    collection = Collection.query.filter_by(collection_ID=collection_id, user_ID=current_user.user_ID).first_or_404()
    card = Card.query.get_or_404(card_id)
    
    exists = CollectionCard.query.filter_by(collection_ID=collection.collection_ID, card_ID=card.card_ID).first()
    if not exists:
        new_link = CollectionCard(collection_ID=collection.collection_ID, card_ID=card.card_ID)
        db.session.add(new_link)
        db.session.commit()
    
    return redirect(url_for('view_collection_cards', collection_id=collection.collection_ID))


