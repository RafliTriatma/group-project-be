from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import config
from utils.database import init_app as init_db

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    CORS(app)
    JWTManager(app)
    init_db(app)
    
    # Import models to ensure they are registered with SQLAlchemy
    from app import models
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app 