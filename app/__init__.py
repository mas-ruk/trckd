from flask import Flask
from .config import DeploymentConfig, TestConfig
from .extensions import db, login_manager, migrate
from .models import User
from .routes import main_bp

config_map = {
    'test': TestConfig,
    'deployment': DeploymentConfig,
}

def create_app(config_name='deployment'):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = ''
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.register_blueprint(main_bp)

    return app
