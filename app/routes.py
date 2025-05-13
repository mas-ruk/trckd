from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, login, db
from app.models import User


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
    from app.models import Card
    return render_template('visualize_data.html')

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

