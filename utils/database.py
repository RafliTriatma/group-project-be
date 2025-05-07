from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, MetaData
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from flask_migrate import Migrate
import logging
from datetime import datetime
import uuid

# Define naming convention for constraints
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Initialize SQLAlchemy with naming convention
db = SQLAlchemy(metadata=MetaData(naming_convention=convention))
migrate = Migrate()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(app):
    """Initialize the database with the Flask app."""
    try:
        # Initialize SQLAlchemy with the app
        db.init_app(app)
        
        # Initialize Flask-Migrate
        migrate.init_app(app, db)
        
        # Enable foreign key support for SQLite
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
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
        """Save the model instance to the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving model: {str(e)}")
            return False
    
    def delete(self):
        """Delete the model instance from the database."""
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
        """Get a model instance by its ID."""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """Get all instances of the model."""
        return cls.query.all()
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def get_db():
    """Get the database session."""
    return db.session

def close_db(e=None):
    """Close the database session."""
    db.session.remove()

def init_app(app):
    """Initialize the database with the Flask app."""
    init_db(app)
    
    # Register database cleanup
    app.teardown_appcontext(close_db)