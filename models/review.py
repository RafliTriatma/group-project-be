import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, Boolean, ForeignKey, Enum, CheckConstraint, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import db, BaseModel
import enum

class Review(BaseModel):
    """Review model for product reviews."""
    __tablename__ = 'reviews'
    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
        {'extend_existing': True}
    )
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)  # To ensure only purchased products can be reviewed
    title = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    is_verified_purchase = db.Column(db.Boolean, default=True)  # Since we link to order_id
    is_helpful = db.Column(db.Integer, default=0)  # Count of helpful votes
    is_visible = db.Column(db.Boolean, default=True)  # For moderation
    
    # Relationships
    user = db.relationship('User', backref='reviews')
    product = db.relationship('Product', backref='reviews')
    order = db.relationship('Order', backref='review')
    review_images = db.relationship('ReviewImage', back_populates='review', cascade='all, delete-orphan')
    helpful_votes = db.relationship('ReviewHelpfulVote', back_populates='review', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert review instance to dictionary."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'product_id': self.product_id,
            'order_id': self.order_id,
            'title': self.title,
            'content': self.content,
            'rating': self.rating,
            'is_verified_purchase': self.is_verified_purchase,
            'is_helpful': self.is_helpful,
            'is_visible': self.is_visible,
            'user': self.user.to_dict() if self.user else None,
            'product': self.product.to_dict() if self.product else None,
            'review_images': [image.to_dict() for image in self.review_images] if self.review_images else [],
            'helpful_votes': [vote.to_dict() for vote in self.helpful_votes] if self.helpful_votes else []
        })
        return data

class ReviewImage(BaseModel):
    """Model for storing review images."""
    __tablename__ = 'review_images'
    __table_args__ = {'extend_existing': True}
    
    review_id = db.Column(db.String(36), db.ForeignKey('reviews.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    
    # Relationships
    review = db.relationship('Review', back_populates='review_images')
    
    def to_dict(self):
        """Convert review image instance to dictionary."""
        data = super().to_dict()
        data.update({
            'review_id': self.review_id,
            'image_url': self.image_url
        })
        return data

class ReviewHelpfulVote(BaseModel):
    """Model for tracking helpful votes on reviews."""
    __tablename__ = 'review_helpful_votes'
    __table_args__ = {'extend_existing': True}
    
    review_id = db.Column(db.String(36), db.ForeignKey('reviews.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    is_helpful = db.Column(db.Boolean, nullable=False)  # True for helpful, False for not helpful
    
    # Relationships
    review = db.relationship('Review', back_populates='helpful_votes')
    user = db.relationship('User', backref='review_votes')
    
    def to_dict(self):
        """Convert review helpful vote instance to dictionary."""
        data = super().to_dict()
        data.update({
            'review_id': self.review_id,
            'user_id': self.user_id,
            'is_helpful': self.is_helpful
        })
        return data

class Rating(BaseModel):
    """Product rating model."""
    __tablename__ = 'ratings'
    __table_args__ = {'extend_existing': True}
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    
    def to_dict(self):
        """Convert rating instance to dictionary."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'product_id': self.product_id,
            'rating': self.rating
        })
        return data 