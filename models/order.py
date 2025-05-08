import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, Boolean, ForeignKey, Enum, CheckConstraint, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import db, BaseModel
import enum

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(enum.Enum):
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    E_WALLET = "e_wallet"
    CASH_ON_DELIVERY = "cash_on_delivery"

class Order(BaseModel):
    """Order model for e-commerce orders."""
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}
    
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0)  # Total discount amount applied
    final_amount = db.Column(db.Float, nullable=False)  # Total amount after discounts
    voucher_id = db.Column(db.String(36), db.ForeignKey('vouchers.id'), nullable=True)
    shipping_address = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='orders')
    order_items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    payment = db.relationship('Payment', back_populates='order', uselist=False)
    voucher = db.relationship('Voucher', back_populates='orders')
    
    def to_dict(self):
        """Convert order instance to dictionary."""
        data = super().to_dict()
        data.update({
            'order_number': self.order_number,
            'total_amount': self.total_amount,
            'discount_amount': self.discount_amount,
            'final_amount': self.final_amount,
            'voucher_id': self.voucher_id,
            'shipping_address': self.shipping_address,
            'status': self.status.value if self.status else None,
            'notes': self.notes,
            'user_id': self.user_id,
            'order_items': [item.to_dict() for item in self.order_items] if self.order_items else [],
            'payment': self.payment.to_dict() if self.payment else None,
            'voucher': self.voucher.to_dict() if self.voucher else None
        })
        return data

class OrderItem(BaseModel):
    """Order item model for individual items in an order."""
    __tablename__ = 'order_items'
    __table_args__ = {'extend_existing': True}
    
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Float, nullable=False)  # Price when order was made
    
    # Relationships
    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product')
    
    def to_dict(self):
        """Convert order item instance to dictionary."""
        data = super().to_dict()
        data.update({
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price_at_time': self.price_at_time,
            'product': self.product.to_dict() if self.product else None
        })
        return data

class Payment(BaseModel):
    """Payment model for order payments."""
    __tablename__ = 'payments'
    __table_args__ = {'extend_existing': True}
    
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.Enum(PaymentMethod), nullable=False)
    status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = db.Column(db.String(100), nullable=True)  # For external payment provider reference
    payment_proof = db.Column(db.String(255), nullable=True)  # URL to payment proof image
    payment_date = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    order = db.relationship('Order', back_populates='payment')
    
    def to_dict(self):
        """Convert payment instance to dictionary."""
        data = super().to_dict()
        data.update({
            'order_id': self.order_id,
            'amount': self.amount,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'status': self.status.value if self.status else None,
            'transaction_id': self.transaction_id,
            'payment_proof': self.payment_proof,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None
        })
        return data 