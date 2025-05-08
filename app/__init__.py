from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import config
from utils.database import init_app as init_db

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Determine configuration based on environment
    if config_name not in config:
        config_name = 'default'
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    CORS(app)
    JWTManager(app)
    
    # Initialize database
    init_db(app)
    
    # Import and register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Import models after database initialization
    with app.app_context():
        import models  # Import from root models directory
        from utils.database import db
        db.create_all()
    
    return app 