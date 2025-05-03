from flask import render_template, request, redirect, url_for
from flask_login import login_user
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, login, db
from app.models import User

@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    register_form = RegisterForm()
    resubmit = False

    if register_form.validate_on_submit() and register_form.form_name.data == 'register_form':
        email = register_form.email.data
        username = register_form.username.data
        password = register_form.password.data

        users = User.query.all()

        for user in users:
            if email == user.email:
                register_form.email.errors.append("Email already in use. Choose a different email.")
                resubmit = True

            if username == user.username:
                register_form.username.errors.append("Username already in use. Choose a different username.")
                resubmit = True

        if not resubmit:
            new_user = User(email=email, username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('collection'))

    elif login_form.validate_on_submit() and login_form.form_name.data == 'login_form':
        email = login_form.email.data
        password = login_form.password.data
        
        user = User.query.filter_by(email=email).first()

        if user == None:
            login_form.email.errors.append("No user registered to that email address.")
            resubmit = True
        if not check_password_hash(user.password, password):
            login_form.password.errors.append("Incorrect password.")
            resubmit = True

        if not resubmit:
            login_user(user)
            return redirect(url_for('collection'))

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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))