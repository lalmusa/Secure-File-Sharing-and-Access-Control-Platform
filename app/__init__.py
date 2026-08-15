from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)

    # Basic configuration
#   app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config.from_object("config.Config")

    # Import Routes
    from app.auth.routes import auth
    from app.files.routes import files
    from app.admin.routes import admin

    # Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(files)
    app.register_blueprint(admin)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    bcrypt.init_app(app)
    # Create database
    from app import models

    @app.route("/")
    def home():
        return "Secure File Sharing Platform is running!"
    
    return app