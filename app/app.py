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


