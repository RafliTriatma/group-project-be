from utils.database import db, BaseModel
from datetime import datetime

class Review(BaseModel):
    """Product review model."""
    __tablename__ = 'reviews'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    title = db.Column(db.String(100))
    comment = db.Column(db.Text)
    is_verified_purchase = db.Column(db.Boolean, default=True)
    helpful_votes = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        """Convert review instance to dictionary."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'product_id': self.product_id,
            'order_id': self.order_id,
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'is_verified_purchase': self.is_verified_purchase,
            'helpful_votes': self.helpful_votes
        })
        return data

class Rating(BaseModel):
    """Product rating model."""
    __tablename__ = 'ratings'
    
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