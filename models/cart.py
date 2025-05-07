from utils.database import db, BaseModel
from datetime import datetime

class Cart(BaseModel):
    """Shopping cart model."""
    __tablename__ = 'carts'
    
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
    """Shopping cart item model."""
    __tablename__ = 'cart_items'
    
    cart_id = db.Column(db.String(36), db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price at time of adding to cart
    
    def to_dict(self):
        """Convert cart item instance to dictionary."""
        data = super().to_dict()
        data.update({
            'cart_id': self.cart_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else 0,
            'subtotal': float(self.price * self.quantity) if self.price else 0
        })
        return data

class Wishlist(BaseModel):
    """Wishlist model."""
    __tablename__ = 'wishlists'
    
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
    """Wishlist item model."""
    __tablename__ = 'wishlist_items'
    
    wishlist_id = db.Column(db.String(36), db.ForeignKey('wishlists.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert wishlist item instance to dictionary."""
        data = super().to_dict()
        data.update({
            'wishlist_id': self.wishlist_id,
            'product_id': self.product_id,
            'added_at': self.added_at.isoformat() if self.added_at else None
        })
        return data 