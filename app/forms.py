from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo
import email_validator

class LoginForm(FlaskForm):
    form_name = HiddenField(default='login_form')
    email = StringField('Email:', validators=[DataRequired(message='Email is required.'), Email(message='Please enter a valid email address.')])
    password = PasswordField('Password:', validators=[DataRequired(message='Password is required.')])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    form_name = HiddenField(default='register_form')
    email = StringField('Email:', validators=[DataRequired(message='Email is required.'), Email(message='Please enter a valid email address.')])
    username = StringField('Username:', validators=[DataRequired(message='Username is required.')])
    password = PasswordField('Password:', validators=[DataRequired(message='Password is required'), EqualTo('password_confirm', message='Passwords must match.')])
    password_confirm = PasswordField('Confirm Password:', validators=[DataRequired(message='Confirmation of password is required.')])
    submit = SubmitField('Register')