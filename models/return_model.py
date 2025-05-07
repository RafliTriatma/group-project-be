from utils.database import db, BaseModel
from datetime import datetime
import enum

class ReturnStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ReturnReason(enum.Enum):
    WRONG_ITEM = "wrong_item"
    DAMAGED = "damaged"
    DEFECTIVE = "defective"
    NOT_AS_DESCRIBED = "not_as_described"
    SIZE_ISSUE = "size_issue"
    QUALITY_ISSUE = "quality_issue"
    OTHER = "other"

class Return(BaseModel):
    """Return model for product returns."""
    __tablename__ = 'returns'
    
    # Basic information
    return_number = db.Column(db.String(50), unique=True, nullable=False)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(ReturnStatus), default=ReturnStatus.PENDING)
    reason = db.Column(db.Enum(ReturnReason), nullable=False)
    description = db.Column(db.Text)
    
    # Shipping information
    return_shipping_address = db.Column(db.Text, nullable=False)
    tracking_number = db.Column(db.String(50))
    return_date = db.Column(db.DateTime)
    
    # Financial information
    refund_amount = db.Column(db.Numeric(10, 2))
    is_partial_return = db.Column(db.Boolean, default=False)
    
    # Relationships
    items = db.relationship('ReturnItem', backref='return', lazy=True, cascade='all, delete-orphan')
    refunds = db.relationship('Refund', backref='return', lazy=True)
    images = db.relationship('ReturnImage', backref='return', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert return instance to dictionary."""
        data = super().to_dict()
        data.update({
            'return_number': self.return_number,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'status': self.status.value if self.status else None,
            'reason': self.reason.value if self.reason else None,
            'description': self.description,
            'return_shipping_address': self.return_shipping_address,
            'tracking_number': self.tracking_number,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'refund_amount': float(self.refund_amount) if self.refund_amount else None,
            'is_partial_return': self.is_partial_return,
            'items': [item.to_dict() for item in self.items],
            'refunds': [refund.to_dict() for refund in self.refunds],
            'images': [image.to_dict() for image in self.images]
        })
        return data

class ReturnItem(BaseModel):
    """Return item model."""
    __tablename__ = 'return_items'
    
    return_id = db.Column(db.String(36), db.ForeignKey('returns.id'), nullable=False)
    order_item_id = db.Column(db.String(36), db.ForeignKey('order_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Enum(ReturnReason), nullable=False)
    
    def to_dict(self):
        """Convert return item instance to dictionary."""
        data = super().to_dict()
        data.update({
            'return_id': self.return_id,
            'order_item_id': self.order_item_id,
            'quantity': self.quantity,
            'reason': self.reason.value if self.reason else None
        })
        return data

class ReturnImage(BaseModel):
    """Return image model."""
    __tablename__ = 'return_images'
    
    return_id = db.Column(db.String(36), db.ForeignKey('returns.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    
    def to_dict(self):
        """Convert return image instance to dictionary."""
        data = super().to_dict()
        data.update({
            'return_id': self.return_id,
            'image_url': self.image_url,
            'description': self.description
        })
        return data

class Refund(BaseModel):
    """Refund model."""
    __tablename__ = 'refunds'
    
    return_id = db.Column(db.String(36), db.ForeignKey('returns.id'), nullable=False)
    payment_id = db.Column(db.String(36), db.ForeignKey('payments.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum(ReturnStatus), default=ReturnStatus.PENDING)
    refund_reason = db.Column(db.Text)
    refund_date = db.Column(db.DateTime)
    transaction_id = db.Column(db.String(100))
    
    def to_dict(self):
        """Convert refund instance to dictionary."""
        data = super().to_dict()
        data.update({
            'return_id': self.return_id,
            'payment_id': self.payment_id,
            'amount': float(self.amount) if self.amount else 0,
            'status': self.status.value if self.status else None,
            'refund_reason': self.refund_reason,
            'refund_date': self.refund_date.isoformat() if self.refund_date else None,
            'transaction_id': self.transaction_id
        })
        return data 