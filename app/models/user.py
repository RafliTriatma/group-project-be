import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import db, BaseModel
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    SELLER = "seller"
    CUSTOMER = "customer"

class User(BaseModel):
    """User model for authentication and user management."""
    __tablename__ = 'users'
    
    # Basic information
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    
    # Role and status
    role = db.Column(db.Enum(UserRole), default=UserRole.CUSTOMER)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    
    # Profile information
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    
    # Relationships
    products = db.relationship('Product', backref='seller', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)
    cart = db.relationship('Cart', backref='user', uselist=False, lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', uselist=False, lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    auth_tokens = db.relationship('AuthToken', back_populates='user', lazy=True)
    
    def to_dict(self):
        """Convert user instance to dictionary."""
        data = super().to_dict()
        data.update({
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'role': self.role.value if self.role else None,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code
        })
        return data

class UserVerification(BaseModel):
    """Model for storing user verification tokens."""
    __tablename__ = 'user_verifications'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    token_type = db.Column(db.String(20), nullable=False)  # email, password_reset, etc.
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        """Convert verification instance to dictionary."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'token_type': self.token_type,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_used': self.is_used
        })
        return data

class AuthToken(BaseModel):
    __tablename__ = 'auth_tokens'

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    token_type = db.Column(db.String(20), nullable=False)  # access, refresh, etc.
    expires_at = db.Column(db.DateTime, nullable=False)
    is_revoked = db.Column(db.Boolean, default=False)

    # Relationship with User
    user = db.relationship('User', back_populates='auth_tokens')

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'token_type': self.token_type,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_revoked': self.is_revoked
        })
        return data 