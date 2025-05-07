from utils.database import db, BaseModel
from datetime import datetime
import enum

class VoucherType(enum.Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    FREE_SHIPPING = "free_shipping"

class VoucherStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"

class Voucher(BaseModel):
    """Voucher model for promotions and discounts."""
    __tablename__ = 'vouchers'
    
    code = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.Enum(VoucherType), nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)  # Percentage or fixed amount
    min_purchase = db.Column(db.Numeric(10, 2), default=0)
    max_discount = db.Column(db.Numeric(10, 2))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(VoucherStatus), default=VoucherStatus.ACTIVE)
    usage_limit = db.Column(db.Integer)  # Total number of times voucher can be used
    usage_count = db.Column(db.Integer, default=0)  # Number of times voucher has been used
    is_single_use = db.Column(db.Boolean, default=False)  # Can be used only once per user
    
    def to_dict(self):
        """Convert voucher instance to dictionary."""
        data = super().to_dict()
        data.update({
            'code': self.code,
            'type': self.type.value if self.type else None,
            'value': float(self.value) if self.value else 0,
            'min_purchase': float(self.min_purchase) if self.min_purchase else 0,
            'max_discount': float(self.max_discount) if self.max_discount else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status.value if self.status else None,
            'usage_limit': self.usage_limit,
            'usage_count': self.usage_count,
            'is_single_use': self.is_single_use
        })
        return data

class Discount(BaseModel):
    """Discount model for product-specific discounts."""
    __tablename__ = 'discounts'
    
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    type = db.Column(db.Enum(VoucherType), nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)  # Percentage or fixed amount
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(VoucherStatus), default=VoucherStatus.ACTIVE)
    min_quantity = db.Column(db.Integer, default=1)  # Minimum quantity to get discount
    
    def to_dict(self):
        """Convert discount instance to dictionary."""
        data = super().to_dict()
        data.update({
            'product_id': self.product_id,
            'type': self.type.value if self.type else None,
            'value': float(self.value) if self.value else 0,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status.value if self.status else None,
            'min_quantity': self.min_quantity
        })
        return data 