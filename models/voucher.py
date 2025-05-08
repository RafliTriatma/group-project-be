import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import db, BaseModel
import enum

class DiscountType(enum.Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"

class VoucherType(enum.Enum):
    SINGLE_USE = "single_use"
    MULTIPLE_USE = "multiple_use"
    UNLIMITED = "unlimited"

class VoucherStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    USED = "used"

class Voucher(BaseModel):
    """Voucher model."""
    __tablename__ = 'vouchers'
    __table_args__ = {'extend_existing': True}

    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    discount_type = db.Column(db.Enum(DiscountType), nullable=False)
    discount_value = db.Column(db.Float, nullable=False)  # Percentage or fixed amount
    min_purchase_amount = db.Column(db.Float, nullable=True)  # Minimum order amount to use voucher
    max_discount_amount = db.Column(db.Float, nullable=True)  # Maximum discount amount for percentage discounts
    voucher_type = db.Column(db.Enum(VoucherType), nullable=False)
    usage_limit = db.Column(db.Integer, nullable=True)  # For multiple_use vouchers
    usage_count = db.Column(db.Integer, default=0)  # Track number of times used
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    orders = db.relationship('Order', back_populates='voucher')

    def to_dict(self):
        """Convert voucher instance to dictionary."""
        data = super().to_dict()
        data.update({
            'code': self.code,
            'description': self.description,
            'discount_type': self.discount_type.value if self.discount_type else None,
            'discount_value': self.discount_value,
            'min_purchase_amount': self.min_purchase_amount,
            'max_discount_amount': self.max_discount_amount,
            'voucher_type': self.voucher_type.value if self.voucher_type else None,
            'usage_limit': self.usage_limit,
            'usage_count': self.usage_count,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active
        })
        return data

class Discount(BaseModel):
    """Discount model."""
    __tablename__ = 'discounts'
    __table_args__ = {'extend_existing': True}

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    discount_type = db.Column(db.Enum(DiscountType), nullable=False)
    discount_value = db.Column(db.Float, nullable=False)  # Percentage or fixed amount
    min_purchase_amount = db.Column(db.Float, nullable=True)
    max_discount_amount = db.Column(db.Float, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        """Convert discount instance to dictionary."""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'discount_type': self.discount_type.value if self.discount_type else None,
            'discount_value': self.discount_value,
            'min_purchase_amount': self.min_purchase_amount,
            'max_discount_amount': self.max_discount_amount,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active
        })
        return data 