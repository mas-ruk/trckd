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
                'card_ID': card.card_ID,
                'name': card.name,
                'type_line': card.type_line or 'Unknown',
                'colors': card.color_identity.split(',') if card.color_identity else [],
                'rarity': card.rarity or 'common',
                'image_uris': image_uris,
                'acquisition_price': card.acquisition_price or 'N/A',
                'current_price': card.current_price or 'N/A'
            }
            
            # Calculate price difference for display
            if card.acquisition_price and card.current_price:
                try:
                    acq_price = float(card.acquisition_price)
                    curr_price = float(card.current_price)
                    diff = curr_price - acq_price
                    percent = (diff / acq_price) * 100 if acq_price else 0
                    
                    card_data['price_difference'] = diff
                    card_data['price_percent'] = percent
                except ValueError:
                    card_data['price_difference'] = None
                    card_data['price_percent'] = None
            
            cards_with_images.append(card_data)
        except Exception as e:
            print(f"Error processing card {card.name}: {str(e)}")
            continue

    # Calculate statistics for the collection
    type_stats = calculate_type_stats(cards_with_images)
    color_stats = calculate_color_stats(cards_with_images)
    rarity_stats = calculate_rarity_stats(cards_with_images)
    financial_stats = calculate_financial_stats(cards_with_images)
    
    return render_template('visualize_data.html', 
                          cards=cards_with_images,
                          type_stats=type_stats,
                          color_stats=color_stats,
                          rarity_stats=rarity_stats,
                          financial_stats=financial_stats)

def calculate_type_stats(cards):
    """Calculate statistics for card types."""
    # Count card types
    type_counts = {
        'Creatures': 0,
        'Instants': 0,
        'Sorceries': 0,
        'Lands': 0,
        'Artifacts': 0,
        'Enchantments': 0,
        'Planeswalkers': 0,
        'Other': 0
    }
    
    # Icons and colors for each type
    type_metadata = {
        'Creatures': {'icon': 'fa-dragon', 'color': '#e74c3c'},
        'Instants': {'icon': 'fa-bolt', 'color': '#3498db'},
        'Sorceries': {'icon': 'fa-magic', 'color': '#9b59b6'},
        'Lands': {'icon': 'fa-mountain', 'color': '#2ecc71'},
        'Artifacts': {'icon': 'fa-cog', 'color': '#95a5a6'},
        'Enchantments': {'icon': 'fa-scroll', 'color': '#f1c40f'},
        'Planeswalkers': {'icon': 'fa-crown', 'color': '#e67e22'},
        'Other': {'icon': 'fa-question-circle', 'color': '#7f8c8d'}
    }
    
    total_cards = len(cards)
    
    # Count types based on type_line content
    for card in cards:
        type_line = card['type_line'].lower()
        if 'creature' in type_line:
            type_counts['Creatures'] += 1
        elif 'instant' in type_line:
            type_counts['Instants'] += 1
        elif 'sorcery' in type_line:
            type_counts['Sorceries'] += 1
        elif 'land' in type_line:
            type_counts['Lands'] += 1
        elif 'artifact' in type_line:
            type_counts['Artifacts'] += 1
        elif 'enchantment' in type_line:
            type_counts['Enchantments'] += 1
        elif 'planeswalker' in type_line:
            type_counts['Planeswalkers'] += 1
        else:
            type_counts['Other'] += 1
    
    # Calculate percentages and combine with metadata
    result = {}
    for type_name, count in type_counts.items():
        if total_cards > 0:
            percentage = (count / total_cards) * 100
        else:
            percentage = 0
            
        result[type_name] = {
            'count': count,
            'percentage': percentage,
            'icon': type_metadata[type_name]['icon'],
            'color': type_metadata[type_name]['color']
        }
    
    return result

def calculate_color_stats(cards):
    """Calculate statistics for card colors."""
    # Count card colors
    color_counts = {
        'White': 0,
        'Blue': 0,
        'Black': 0,
        'Red': 0,
        'Green': 0,
        'Multicolor': 0,
        'Colorless': 0
    }
    
    # Icons and colors for each color
    color_metadata = {
        'White': {'icon': 'fa-sun', 'color': '#f0e6d2'},
        'Blue': {'icon': 'fa-tint', 'color': '#0e6cbb'},
        'Black': {'icon': 'fa-skull', 'color': '#393939'},
        'Red': {'icon': 'fa-fire', 'color': '#d32f2f'},
        'Green': {'icon': 'fa-leaf', 'color': '#4caf50'},
        'Multicolor': {'icon': 'fa-palette', 'color': '#ffd700'},
        'Colorless': {'icon': 'fa-cube', 'color': '#9e9e9e'}
    }
    
    total_cards = len(cards)
    
    # Count colors based on the colors field
    for card in cards:
        colors = card['colors']
        if not colors:
            color_counts['Colorless'] += 1
        elif len(colors) > 1:
            color_counts['Multicolor'] += 1
        elif 'W' in colors:
            color_counts['White'] += 1
        elif 'U' in colors:
            color_counts['Blue'] += 1
        elif 'B' in colors:
            color_counts['Black'] += 1
        elif 'R' in colors:
            color_counts['Red'] += 1
        elif 'G' in colors:
            color_counts['Green'] += 1
    
    # Calculate percentages and combine with metadata
    result = {}
    for color_name, count in color_counts.items():
        if total_cards > 0:
            percentage = (count / total_cards) * 100
        else:
            percentage = 0
            
        result[color_name] = {
            'count': count,
            'percentage': percentage,
            'icon': color_metadata[color_name]['icon'],
            'color': color_metadata[color_name]['color']
        }
    
    return result

def calculate_rarity_stats(cards):
    """Calculate statistics for card rarities."""
    # Count card rarities
    rarity_counts = {
        'Common': 0,
        'Uncommon': 0,
        'Rare': 0,
        'Mythic': 0,
        'Special': 0
    }
    
    # Icons and colors for each rarity
    rarity_metadata = {
        'Common': {'icon': 'fa-circle', 'color': '#bdc3c7'},
        'Uncommon': {'icon': 'fa-circle', 'color': '#95a5a6'},
        'Rare': {'icon': 'fa-star', 'color': '#f1c40f'},
        'Mythic': {'icon': 'fa-gem', 'color': '#e74c3c'},
        'Special': {'icon': 'fa-certificate', 'color': '#9b59b6'}
    }
    
    total_cards = len(cards)
    
    # Count rarities
    for card in cards:
        rarity = card['rarity'].lower().capitalize()
        if rarity in rarity_counts:
            rarity_counts[rarity] += 1
        else:
            rarity_counts['Special'] += 1
    
    # Calculate percentages and combine with metadata
    result = {}
    for rarity_name, count in rarity_counts.items():
        if total_cards > 0:
            percentage = (count / total_cards) * 100
        else:
            percentage = 0
            
        result[rarity_name] = {
            'count': count,
            'percentage': percentage,
            'icon': rarity_metadata[rarity_name]['icon'],
            'color': rarity_metadata[rarity_name]['color']
        }
    
    return result

def calculate_financial_stats(cards):
    """Calculate financial statistics for the collection."""
    total_acquisition = 0.0
    total_current = 0.0
    valid_card_count = 0
    
    for card in cards:
        try:
            if card['acquisition_price'] != 'N/A' and card['current_price'] != 'N/A':
                acquisition_price = float(card['acquisition_price'])
                current_price = float(card['current_price'])
                
                total_acquisition += acquisition_price
                total_current += current_price
                valid_card_count += 1
        except (ValueError, TypeError):
            continue
    
    # Calculate growth metrics
    difference = total_current - total_acquisition
    if total_acquisition > 0:
        growth_percent = (difference / total_acquisition) * 100
    else:
        growth_percent = 0
    
    # Add clamped percentage for progress bar
    progress_width = min(max(growth_percent, 0), 100)
    
    # Determine color based on growth
    if difference > 0:
        color = '#4caf50'  # Green for positive growth
        icon = 'fa-chart-line'
    elif difference < 0:
        color = '#d32f2f'  # Red for negative growth
        icon = 'fa-chart-line'
    else:
        color = '#9e9e9e'  # Gray for no change
        icon = 'fa-equals'
    
    return {
        'total_acquisition': total_acquisition,
        'total_current': total_current,
        'difference': difference,
        'growth_percent': growth_percent,
        'progress_width': progress_width,  # Add this new field
        'valid_card_count': valid_card_count,
        'color': color,
        'icon': icon
    }

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
