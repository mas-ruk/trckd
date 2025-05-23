from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    form_name = HiddenField(default='login_form')
    login_email = StringField('Email:', validators=[DataRequired(message='Email is required.'), Email(message='Please enter a valid email address.')])
    login_password = PasswordField('Password:', validators=[DataRequired(message='Password is required.')])
    login_remember_me = BooleanField('Remember Me:')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    form_name = HiddenField(default='register_form')
    register_email = StringField('Email:', validators=[DataRequired(message='Email is required.'), Email(message='Please enter a valid email address.')])
    username = StringField('Username:', validators=[DataRequired(message='Username is required.')])
    register_password = PasswordField('Password:', validators=[DataRequired(message='Password is required'), EqualTo('password_confirm', message='Passwords must match.')])
    password_confirm = PasswordField('Confirm Password:', validators=[DataRequired(message='Confirmation of password is required.')])
    register_remember_me = BooleanField('Remember Me:')
    register_submit = SubmitField('Register')