from flask import render_template, request, redirect, url_for, jsonify, send_file
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, login, db
from app.forms import LoginForm, RegisterForm
from app.models import User, Card, SharedLink
import uuid, json, io

# ------------------------
# Authentication Routes
# ------------------------

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
            new_user = User(
                email=register_email,
                username=username,
                password=generate_password_hash(register_password)
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=register_remember)
            return redirect(url_for('collection'))

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
            return redirect(url_for('collection'))

    return render_template(
        'homepage.html',
        login_form=login_form,
        register_form=register_form,
        active_tab=active_tab
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# ------------------------
# Page Views
# ------------------------

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
    return render_template('visualize_data.html')

# ------------------------
# Share Functionality
# ------------------------

@app.route('/share')
@login_required
def share_page():
    user_cards = Card.query.filter_by(user_ID=current_user.user_ID).all()
    return render_template('share.html', user_cards=user_cards)

@app.route('/generate_share_link', methods=['POST'])
@login_required
def generate_share_link():
    data = request.get_json()
    selected_cards = data.get("cards", [])
    link_id = str(uuid.uuid4())[:8]

    link = SharedLink(link_id=link_id, cards_data=json.dumps(selected_cards))
    db.session.add(link)
    db.session.commit()

    return jsonify({"link_id": link_id})

@app.route('/shared/<link_id>')
def shared_cards(link_id):
    link = SharedLink.query.filter_by(link_id=link_id).first()
    if link:
        cards_data = json.loads(link.cards_data)
        return render_template('shared_cards.html', cards=cards_data)
    return "Link not found", 404

@app.route('/download_shared/<link_id>')
def download_shared(link_id):
    link = SharedLink.query.filter_by(link_id=link_id).first()
    if link:
        cards_data = json.loads(link.cards_data)
        rendered_html = render_template('shared_cards.html', cards=cards_data)
        buffer = io.BytesIO()
        buffer.write(rendered_html.encode())
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"{link_id}.html", mimetype='text/html')
    return "Link not found", 404
