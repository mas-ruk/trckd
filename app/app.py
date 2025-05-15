from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

@app.route('/')
def index():
    return "Hello, Flask is running with config!"

if __name__ == "__main__":
    from models import User, Card, Collection,collection_card
    
   
    print("Flask app is starting...")
    app.run(debug=True)


