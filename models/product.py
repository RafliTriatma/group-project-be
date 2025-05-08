"""Product models for the e-commerce application."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, Boolean, ForeignKey, Enum, CheckConstraint, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import db, BaseModel
import enum

class ProductStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"

class Category(BaseModel):
    """Category model for product categorization."""
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True}
    
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.String(36), db.ForeignKey('categories.id'))
    image_url = db.Column(db.String(255))
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)
    subcategories = db.relationship('Category', backref=db.backref('parent', remote_side='Category.id'), lazy=True)
    
    def to_dict(self):
        """Convert category instance to dictionary."""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'image_url': self.image_url
        })
        return data

class Product(BaseModel):
    """Product model for e-commerce items."""
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}
    
    # Basic information
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(50), unique=True)
    
    # Status and visibility
    status = db.Column(db.Enum(ProductStatus), default=ProductStatus.DRAFT)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Relationships
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    seller_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Product details
    weight = db.Column(db.Float)  # in kg
    dimensions = db.Column(db.String(50))  # format: "LxWxH" in cm
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    
    # Images and media
    main_image = db.Column(db.String(255))
    images = db.relationship('ProductImage', backref='product', lazy=True)
    
    # Related products
    reviews = db.relationship('Review', backref='product', lazy=True)
    ratings = db.relationship('Rating', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    wishlist_items = db.relationship('WishlistItem', backref='product', lazy=True)
    
    def to_dict(self):
        """Convert product instance to dictionary."""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else None,
            'stock': self.stock,
            'sku': self.sku,
            'status': self.status.value if self.status else None,
            'is_featured': self.is_featured,
            'category_id': self.category_id,
            'seller_id': self.seller_id,
            'weight': self.weight,
            'dimensions': self.dimensions,
            'brand': self.brand,
            'model': self.model,
            'main_image': self.main_image
        })
        return data

class ProductImage(BaseModel):
    """Model for storing product images."""
    __tablename__ = 'product_images'
    __table_args__ = {'extend_existing': True}
    
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_main = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        """Convert product image instance to dictionary."""
        data = super().to_dict()
        data.update({
            'product_id': self.product_id,
            'image_url': self.image_url,
            'is_main': self.is_main,
            'display_order': self.display_order
        })
        return data 