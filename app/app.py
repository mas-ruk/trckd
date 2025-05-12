from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config 

app = Flask(__name__)
app.config.from_object(Config)  
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Hello, Flask is running with config!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database and tables
    print("Flask app is starting...")
    app.run(debug=True)

