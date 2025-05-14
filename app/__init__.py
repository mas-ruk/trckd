from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

# Initialize the app and extensions
app = Flask(__name__)
app.config.from_object(Config)

# Set up the database and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set up the login manager
login = LoginManager(app)
login.login_view = 'index'  

# Import routes and models after app and db are set up
from app import routes, models

