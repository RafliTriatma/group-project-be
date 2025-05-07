from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
import logging
from datetime import datetime
import uuid

# Initialize SQLAlchemy
db = SQLAlchemy()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(app):
    """Initialize the database with the Flask app."""
    try:
        # Initialize SQLAlchemy with app
        db.init_app(app)
        
        # Enable foreign key support for SQLite
        @event.listens_for(Engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            if isinstance(dbapi_connection, SQLite3Connection):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON;")
                cursor.close()
        
        # Create all tables
        with app.app_context():
            db.create_all()
            logger.info("Database initialized successfully")
            
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

class BaseModel(db.Model):
    """Base model class that includes common fields and methods."""
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Save the model instance."""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving model: {str(e)}")
            return False
    
    def delete(self):
        """Delete the model instance."""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting model: {str(e)}")
            return False
    
    @classmethod
    def get_by_id(cls, id):
        """Get a model instance by ID."""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """Get all model instances."""
        return cls.query.all()
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def get_db():
    """Get database session."""
    return db.session

def close_db(e=None):
    """Close database session."""
    db.session.remove()

def init_app(app):
    """Initialize the database with the Flask app."""
    init_db(app)
    
    # Register database cleanup
    app.teardown_appcontext(close_db)