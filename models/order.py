from utils.database import db, BaseModel
from datetime import datetime
import enum

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    E_WALLET = "e_wallet"
    CASH_ON_DELIVERY = "cash_on_delivery"

class Order(BaseModel):
    """Order model for customer purchases."""
    __tablename__ = 'orders'
    
    # Basic information
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    
    # Shipping information
    shipping_address = db.Column(db.Text, nullable=False)
    shipping_city = db.Column(db.String(50), nullable=False)
    shipping_state = db.Column(db.String(50), nullable=False)
    shipping_country = db.Column(db.String(50), nullable=False)
    shipping_postal_code = db.Column(db.String(20), nullable=False)
    tracking_number = db.Column(db.String(50))
    
    # Financial information
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tax = db.Column(db.Numeric(10, 2), default=0)
    shipping_cost = db.Column(db.Numeric(10, 2), default=0)
    discount = db.Column(db.Numeric(10, 2), default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Timestamps
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_date = db.Column(db.DateTime)
    shipping_date = db.Column(db.DateTime)
    delivery_date = db.Column(db.DateTime)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='order', lazy=True)
    returns = db.relationship('Return', backref='order', lazy=True)
    
    def to_dict(self):
        """Convert order instance to dictionary."""
        data = super().to_dict()
        data.update({
            'order_number': self.order_number,
            'user_id': self.user_id,
            'status': self.status.value if self.status else None,
            'shipping_address': self.shipping_address,
            'shipping_city': self.shipping_city,
            'shipping_state': self.shipping_state,
            'shipping_country': self.shipping_country,
            'shipping_postal_code': self.shipping_postal_code,
            'tracking_number': self.tracking_number,
            'subtotal': float(self.subtotal) if self.subtotal else 0,
            'tax': float(self.tax) if self.tax else 0,
            'shipping_cost': float(self.shipping_cost) if self.shipping_cost else 0,
            'discount': float(self.discount) if self.discount else 0,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'shipping_date': self.shipping_date.isoformat() if self.shipping_date else None,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'items': [item.to_dict() for item in self.items],
            'payments': [payment.to_dict() for payment in self.payments]
        })
        return data

class OrderItem(BaseModel):
    """Order item model."""
    __tablename__ = 'order_items'
    
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price at time of order
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    def to_dict(self):
        """Convert order item instance to dictionary."""
        data = super().to_dict()
        data.update({
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else 0,
            'subtotal': float(self.subtotal) if self.subtotal else 0
        })
        return data

class Payment(BaseModel):
    """Payment model."""
    __tablename__ = 'payments'
    
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING)
    method = db.Column(db.Enum(PaymentMethod), nullable=False)
    transaction_id = db.Column(db.String(100))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    refunds = db.relationship('Refund', backref='payment', lazy=True)
    
    def to_dict(self):
        """Convert payment instance to dictionary."""
        data = super().to_dict()
        data.update({
            'order_id': self.order_id,
            'amount': float(self.amount) if self.amount else 0,
            'status': self.status.value if self.status else None,
            'method': self.method.value if self.method else None,
            'transaction_id': self.transaction_id,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None
        })
        return data 