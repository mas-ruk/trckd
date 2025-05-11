import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SECRET_KEY = "a_secret_key"
    SQLALCHEMY_TRACK_MODIFICATION = False

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or default_database_location

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"
    TESTING = True
