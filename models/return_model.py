import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import db, BaseModel
import enum

class ReturnStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ReturnReason(enum.Enum):
    DAMAGED = "damaged"
    WRONG_ITEM = "wrong_item"
    QUALITY_ISSUE = "quality_issue"
    SIZE_ISSUE = "size_issue"
    COLOR_ISSUE = "color_issue"
    NOT_AS_DESCRIBED = "not_as_described"
    OTHER = "other"

class RefundStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Return(BaseModel):
    """Return request model."""
    __tablename__ = 'returns'
    __table_args__ = {'extend_existing': True}

    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    return_number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.Enum(ReturnStatus), default=ReturnStatus.PENDING)
    reason = db.Column(db.Enum(ReturnReason), nullable=False)
    description = db.Column(db.Text, nullable=False)
    return_shipping_address = db.Column(db.Text, nullable=False)
    tracking_number = db.Column(db.String(100), nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    refund_amount = db.Column(db.Float, nullable=False)
    is_partial_return = db.Column(db.Boolean, default=False)

    # Relationships
    order = db.relationship('Order', backref='returns')
    user = db.relationship('User', backref='returns')
    return_items = db.relationship('ReturnItem', back_populates='return_request', cascade='all, delete-orphan')
    refund = db.relationship('Refund', back_populates='return_request', uselist=False)
    return_images = db.relationship('ReturnImage', back_populates='return_request', cascade='all, delete-orphan')

    def to_dict(self):
        """Convert return request instance to dictionary."""
        data = super().to_dict()
        data.update({
            'order_id': self.order_id,
            'user_id': self.user_id,
            'return_number': self.return_number,
            'status': self.status.value if self.status else None,
            'reason': self.reason.value if self.reason else None,
            'description': self.description,
            'return_shipping_address': self.return_shipping_address,
            'tracking_number': self.tracking_number,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'refund_amount': self.refund_amount,
            'is_partial_return': self.is_partial_return,
            'return_items': [item.to_dict() for item in self.return_items],
            'return_images': [image.to_dict() for image in self.return_images],
            'refund': self.refund.to_dict() if self.refund else None
        })
        return data

class ReturnItem(BaseModel):
    """Return item model."""
    __tablename__ = 'return_items'
    __table_args__ = {'extend_existing': True}

    return_id = db.Column(db.String(36), db.ForeignKey('returns.id'), nullable=False)
    order_item_id = db.Column(db.String(36), db.ForeignKey('order_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Enum(ReturnReason), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    return_request = db.relationship('Return', back_populates='return_items')
    order_item = db.relationship('OrderItem')

    def to_dict(self):
        """Convert return item instance to dictionary."""
        data = super().to_dict()
        data.update({
            'return_id': self.return_id,
            'order_item_id': self.order_item_id,
            'quantity': self.quantity,
            'reason': self.reason.value if self.reason else None,
            'description': self.description,
            'order_item': self.order_item.to_dict() if self.order_item else None
        })
        return data

class ReturnImage(BaseModel):
    """Return image model."""
    __tablename__ = 'return_images'
    __table_args__ = {'extend_existing': True}

    return_id = db.Column(db.String(36), db.ForeignKey('returns.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    # Relationships
    return_request = db.relationship('Return', back_populates='return_images')

    def to_dict(self):
        """Convert return image instance to dictionary."""
        data = super().to_dict()
        data.update({
            'return_id': self.return_id,
            'image_url': self.image_url
        })
        return data

class Refund(BaseModel):
    """Refund model."""
    __tablename__ = 'refunds'
    __table_args__ = {'extend_existing': True}

    return_id = db.Column(db.String(36), db.ForeignKey('returns.id'), nullable=False)
    payment_id = db.Column(db.String(36), db.ForeignKey('payments.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(RefundStatus), default=RefundStatus.PENDING)
    refund_reason = db.Column(db.Text, nullable=True)
    refund_date = db.Column(db.DateTime, nullable=True)
    transaction_id = db.Column(db.String(100), nullable=True)  # Reference from payment provider

    # Relationships
    return_request = db.relationship('Return', back_populates='refund')
    payment = db.relationship('Payment', backref='refunds')

    def to_dict(self):
        """Convert refund instance to dictionary."""
        data = super().to_dict()
        data.update({
            'return_id': self.return_id,
            'payment_id': self.payment_id,
            'amount': self.amount,
            'status': self.status.value if self.status else None,
            'refund_reason': self.refund_reason,
            'refund_date': self.refund_date.isoformat() if self.refund_date else None,
            'transaction_id': self.transaction_id
        })
        return data 