from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from .extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
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
                session.permanent = True
                login_user(user, remember=True)
            else:
                session.permanent = False
                login_user(user, remember=False)
            return redirect(url_for('main.collection'))

    elif login_form.submit.data and login_form.validate_on_submit():
        login_email = login_form.login_email.data
        login_password = login_form.login_password.data
        login_remember = login_form.login_remember_me.data
        
        user = User.query.filter_by(email=login_email).first()

        if user == None:
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
            return redirect(url_for('main.collection'))

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
    # Import Card only when this route is accessed
    from app.models import Card
    return render_template('visualize_data.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

