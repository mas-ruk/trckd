# I'm 99% sure we don't need this file since running the Flask app is handled by all the testing stuff I set up, but I'm keeping it here for now.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from models import User, Card

@app.route('/')
def index():
    return "Hello, Flask is running with config!"

if __name__ == "__main__":
    print("Flask app is starting...")
    app.run(debug=True)


