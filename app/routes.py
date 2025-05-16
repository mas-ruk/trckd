import uuid
import time
import json

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    Response
)
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from app.forms import LoginForm, RegisterForm
from .extensions import db
from .models import User, Card, SharedLink

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

# ────────────────────────────────────────────────────────────────
# NEW: API endpoint to add a card for the logged-in user
@main_bp.route('/api/add_card', methods=['POST'])
@login_required
def api_add_card():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify(success=False, message="Missing card name"), 400

    # Build and save the Card linked to current_user
    card = Card(
        name             = name,
        type_line        = data.get('type_line'),
        color_identity   = ','.join(data.get('color_identity', [])),
        rarity           = data.get('rarity'),
        set_code         = data.get('set_code'),
        set_name         = data.get('set_name'),
        collector_number = data.get('collector_number'),
        mana_cost        = data.get('mana_cost'),
        cmc              = data.get('cmc'),
        oracle_text      = data.get('oracle_text'),
        power            = data.get('power'),
        toughness        = data.get('toughness'),
        image_uris       = json.dumps(data.get('image_uris', {})),
        lang             = data.get('lang'),
        user_ID          = current_user.user_ID   # ← link to the user
    )

    db.session.add(card)
    db.session.commit()
    return jsonify(success=True, card_id=card.card_ID)
# ────────────────────────────────────────────────────────────────

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

@main_bp.route('/share')
@login_required
def share():
    user_cards = []
    for c in Card.query.filter_by(user_ID=current_user.user_ID):
        url = ''
        if c.image_uris:
            try:
                data = json.loads(c.image_uris)
                url = data.get('normal', '')
            except:
                pass
        user_cards.append({
            'id':        c.card_ID,
            'name':      c.name,
            'rarity':    c.rarity,
            'image_url': url
        })
    return render_template('share.html', user_cards=user_cards)

@main_bp.route('/generate_share_link', methods=['POST'])
@login_required
def generate_share_link():
    data = request.get_json() or {}
    card_ids = data.get('card_ids', [])

    if not card_ids:
        return jsonify(success=False, message='No cards selected'), 400

    new_link = SharedLink(
        link_id = str(uuid.uuid4()),
        user_ID = current_user.user_ID
    )
    db.session.add(new_link)
    db.session.commit()  

    for cid in card_ids:
        card = Card.query.get(cid)
        if card:
            new_link.cards.append(card)
    db.session.commit()

    share_url = url_for('main.shared_cards', link_id=new_link.link_id, _external=True)
    return jsonify(success=True, link_id=new_link.link_id, share_url=share_url)

@main_bp.route('/shared/<link_id>')
def shared_cards(link_id):
    link = SharedLink.query.filter_by(link_id=link_id).first_or_404()

    cards_to_show = []
    for c in link.cards:
        # default fallback if nothing parses
        image_url = None
        if c.image_uris:
            try:
                data = json.loads(c.image_uris)
                # prefer the 'normal' size, then any other
                image_url = data.get('normal') or next(iter(data.values()))
            except Exception:
                pass

        cards_to_show.append({
            'name':       c.name,
            'type_line':  c.type_line or '',
            'oracle_text': c.oracle_text or 'No description available.',
            'image_url':  image_url or url_for('static', filename='images/placeholder.jpg')
        })

    return render_template('shared_cards.html', cards=cards_to_show)

@main_bp.route('/download_shared/<link_id>')
def download_shared(link_id):
    link = SharedLink.query.filter_by(link_id=link_id).first_or_404()

    cards_to_show = []
    for c in link.cards:
        # parse the JSON you originally stored in image_uris
        try:
            image_data = json.loads(c.image_uris or '{}')
        except ValueError:
            image_data = {}

        # pick the highest-res Scryfall URL you like:
        # for example, art_crop or png if you stored it
        image_url = (
            image_data.get('png') or
            image_data.get('art_crop') or
            image_data.get('normal') or
            url_for('static', filename='images/placeholder.jpg')
        )

        cards_to_show.append({
            'name':        c.name,
            'oracle_text': c.oracle_text or 'No description available.',
            'image_url':   image_url
        })

    html = render_template('shared_cards.html', cards=cards_to_show)
    return Response(
        html,
        mimetype='text/html',
        headers={ 'Content-Disposition': f'attachment; filename=shared-{link_id}.html' }
    )