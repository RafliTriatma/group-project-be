"""Cart and wishlist models for the e-commerce application."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, Boolean, ForeignKey, Enum, CheckConstraint, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import db, BaseModel
import enum

class Cart(BaseModel):
    """Shopping cart model."""
    __tablename__ = 'carts'
    __table_args__ = {'extend_existing': True}
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), default=0)
    
    # Relationships
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert cart instance to dictionary."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'items': [item.to_dict() for item in self.items]
        })
        return data

class CartItem(BaseModel):
    """Cart item model for shopping cart items."""
    __tablename__ = 'cart_items'
    __table_args__ = {'extend_existing': True}
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')
    
    def to_dict(self):
        """Convert cart item instance to dictionary."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product': self.product.to_dict() if self.product else None
        })
        return data

class Wishlist(BaseModel):
    """Wishlist model."""
    __tablename__ = 'wishlists'
    __table_args__ = {'extend_existing': True}
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    items = db.relationship('WishlistItem', backref='wishlist', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert wishlist instance to dictionary."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items]
        })
        return data

class WishlistItem(BaseModel):
    """Wishlist item model for user wishlists."""
    __tablename__ = 'wishlist_items'
    __table_args__ = {'extend_existing': True}
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='wishlist_items')
    product = db.relationship('Product', backref='wishlist_items')
    
    def to_dict(self):
        """Convert wishlist item instance to dictionary."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None
        })
        return data 