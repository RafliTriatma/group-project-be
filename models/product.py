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

class ProductStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"

class Category(BaseModel):
    """Category model for product categorization."""
    __tablename__ = 'categories'
    
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

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship('User', backref='cart_items')
    product = relationship('Product', backref='cart_items')

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'product_id': str(self.product_id),
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'product': self.product.to_dict() if self.product else None
        }

class WishlistItem(db.Model):
    __tablename__ = 'wishlist_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship('User', backref='wishlist_items')
    product = relationship('Product', backref='wishlist_items')

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'product_id': str(self.product_id),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'product': self.product.to_dict() if self.product else None
        }

class DiscountType(enum.Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"

class VoucherType(enum.Enum):
    SINGLE_USE = "single_use"
    MULTIPLE_USE = "multiple_use"
    UNLIMITED = "unlimited"

class Voucher(db.Model):
    __tablename__ = 'vouchers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    discount_type = Column(Enum(DiscountType), nullable=False)
    discount_value = Column(Float, nullable=False)  # Percentage or fixed amount
    min_purchase_amount = Column(Float, nullable=True)  # Minimum order amount to use voucher
    max_discount_amount = Column(Float, nullable=True)  # Maximum discount amount for percentage discounts
    voucher_type = Column(Enum(VoucherType), nullable=False)
    usage_limit = Column(Integer, nullable=True)  # For multiple_use vouchers
    usage_count = Column(Integer, default=0)  # Track number of times used
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    orders = relationship('Order', back_populates='voucher')

    def to_dict(self):
        return {
            'id': str(self.id),
            'code': self.code,
            'description': self.description,
            'discount_type': self.discount_type.value,
            'discount_value': self.discount_value,
            'min_purchase_amount': self.min_purchase_amount,
            'max_discount_amount': self.max_discount_amount,
            'voucher_type': self.voucher_type.value,
            'usage_limit': self.usage_limit,
            'usage_count': self.usage_count,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Discount(db.Model):
    __tablename__ = 'discounts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    discount_type = Column(Enum(DiscountType), nullable=False)
    discount_value = Column(Float, nullable=False)  # Percentage or fixed amount
    min_purchase_amount = Column(Float, nullable=True)
    max_discount_amount = Column(Float, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'discount_type': self.discount_type.value,
            'discount_value': self.discount_value,
            'min_purchase_amount': self.min_purchase_amount,
            'max_discount_amount': self.max_discount_amount,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    order_number = Column(String(50), unique=True, nullable=False)
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0)  # Total discount amount applied
    final_amount = Column(Float, nullable=False)  # Total amount after discounts
    voucher_id = Column(UUID(as_uuid=True), ForeignKey('vouchers.id'), nullable=True)
    shipping_address = Column(Text, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship('User', backref='orders')
    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    payment = relationship('Payment', back_populates='order', uselist=False)
    voucher = relationship('Voucher', back_populates='orders')

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'order_number': self.order_number,
            'total_amount': self.total_amount,
            'discount_amount': self.discount_amount,
            'final_amount': self.final_amount,
            'voucher_id': str(self.voucher_id) if self.voucher_id else None,
            'shipping_address': self.shipping_address,
            'status': self.status.value,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'order_items': [item.to_dict() for item in self.order_items],
            'payment': self.payment.to_dict() if self.payment else None,
            'voucher': self.voucher.to_dict() if self.voucher else None
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_time = Column(Float, nullable=False)  # Price when order was made
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order = relationship('Order', back_populates='order_items')
    product = relationship('Product')

    def to_dict(self):
        return {
            'id': str(self.id),
            'order_id': str(self.order_id),
            'product_id': str(self.product_id),
            'quantity': self.quantity,
            'price_at_time': self.price_at_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'product': self.product.to_dict() if self.product else None
        }

class Payment(db.Model):
    __tablename__ = 'payments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = Column(String(100), nullable=True)  # For external payment provider reference
    payment_proof = Column(String(255), nullable=True)  # URL to payment proof image
    payment_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order = relationship('Order', back_populates='payment')

    def to_dict(self):
        return {
            'id': str(self.id),
            'order_id': str(self.order_id),
            'amount': self.amount,
            'payment_method': self.payment_method.value,
            'status': self.status.value,
            'transaction_id': self.transaction_id,
            'payment_proof': self.payment_proof,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Review(db.Model):
    __tablename__ = 'reviews'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)  # To ensure only purchased products can be reviewed
    title = Column(String(100), nullable=True)
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    is_verified_purchase = Column(Boolean, default=True)  # Since we link to order_id
    is_helpful = Column(Integer, default=0)  # Count of helpful votes
    is_visible = Column(Boolean, default=True)  # For moderation
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship('User', backref='reviews')
    product = relationship('Product', backref='reviews')
    order = relationship('Order', backref='review')
    review_images = relationship('ReviewImage', back_populates='review', cascade='all, delete-orphan')
    helpful_votes = relationship('ReviewHelpfulVote', back_populates='review', cascade='all, delete-orphan')

    # Constraint to ensure rating is between 1 and 5
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'product_id': str(self.product_id),
            'order_id': str(self.order_id),
            'title': self.title,
            'content': self.content,
            'rating': self.rating,
            'is_verified_purchase': self.is_verified_purchase,
            'is_helpful': self.is_helpful,
            'is_visible': self.is_visible,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user': {
                'id': str(self.user.id),
                'username': self.user.username
            } if self.user else None,
            'review_images': [image.to_dict() for image in self.review_images],
            'helpful_votes_count': len(self.helpful_votes)
        }

class ReviewImage(db.Model):
    __tablename__ = 'review_images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id = Column(UUID(as_uuid=True), ForeignKey('reviews.id'), nullable=False)
    image_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    review = relationship('Review', back_populates='review_images')

    def to_dict(self):
        return {
            'id': str(self.id),
            'review_id': str(self.review_id),
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ReviewHelpfulVote(db.Model):
    __tablename__ = 'review_helpful_votes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id = Column(UUID(as_uuid=True), ForeignKey('reviews.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    is_helpful = Column(Boolean, nullable=False)  # True for helpful, False for not helpful
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    review = relationship('Review', back_populates='helpful_votes')
    user = relationship('User', backref='review_votes')

    def to_dict(self):
        return {
            'id': str(self.id),
            'review_id': str(self.review_id),
            'user_id': str(self.user_id),
            'is_helpful': self.is_helpful,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

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

class Return(db.Model):
    __tablename__ = 'returns'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    return_number = Column(String(50), unique=True, nullable=False)
    status = Column(Enum(ReturnStatus), default=ReturnStatus.PENDING)
    reason = Column(Enum(ReturnReason), nullable=False)
    description = Column(Text, nullable=False)
    return_shipping_address = Column(Text, nullable=False)
    tracking_number = Column(String(100), nullable=True)
    return_date = Column(DateTime, nullable=True)
    refund_amount = Column(Float, nullable=False)
    is_partial_return = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order = relationship('Order', backref='returns')
    user = relationship('User', backref='returns')
    return_items = relationship('ReturnItem', back_populates='return_request', cascade='all, delete-orphan')
    refund = relationship('Refund', back_populates='return_request', uselist=False)
    return_images = relationship('ReturnImage', back_populates='return_request', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': str(self.id),
            'order_id': str(self.order_id),
            'user_id': str(self.user_id),
            'return_number': self.return_number,
            'status': self.status.value,
            'reason': self.reason.value,
            'description': self.description,
            'return_shipping_address': self.return_shipping_address,
            'tracking_number': self.tracking_number,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'refund_amount': self.refund_amount,
            'is_partial_return': self.is_partial_return,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'return_items': [item.to_dict() for item in self.return_items],
            'refund': self.refund.to_dict() if self.refund else None,
            'return_images': [image.to_dict() for image in self.return_images]
        }

class ReturnItem(db.Model):
    __tablename__ = 'return_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    return_id = Column(UUID(as_uuid=True), ForeignKey('returns.id'), nullable=False)
    order_item_id = Column(UUID(as_uuid=True), ForeignKey('order_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(Enum(ReturnReason), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    return_request = relationship('Return', back_populates='return_items')
    order_item = relationship('OrderItem')

    def to_dict(self):
        return {
            'id': str(self.id),
            'return_id': str(self.return_id),
            'order_item_id': str(self.order_item_id),
            'quantity': self.quantity,
            'reason': self.reason.value,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'order_item': self.order_item.to_dict() if self.order_item else None
        }

class ReturnImage(db.Model):
    __tablename__ = 'return_images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    return_id = Column(UUID(as_uuid=True), ForeignKey('returns.id'), nullable=False)
    image_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    return_request = relationship('Return', back_populates='return_images')

    def to_dict(self):
        return {
            'id': str(self.id),
            'return_id': str(self.return_id),
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Refund(db.Model):
    __tablename__ = 'refunds'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    return_id = Column(UUID(as_uuid=True), ForeignKey('returns.id'), nullable=False)
    payment_id = Column(UUID(as_uuid=True), ForeignKey('payments.id'), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(RefundStatus), default=RefundStatus.PENDING)
    refund_reason = Column(Text, nullable=True)
    refund_date = Column(DateTime, nullable=True)
    transaction_id = Column(String(100), nullable=True)  # Reference from payment provider
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    return_request = relationship('Return', back_populates='refund')
    payment = relationship('Payment', backref='refunds')

    def to_dict(self):
        return {
            'id': str(self.id),
            'return_id': str(self.return_id),
            'payment_id': str(self.payment_id),
            'amount': self.amount,
            'status': self.status.value,
            'refund_reason': self.refund_reason,
            'refund_date': self.refund_date.isoformat() if self.refund_date else None,
            'transaction_id': self.transaction_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class NotificationType(enum.Enum):
    ORDER_STATUS = "order_status"
    PAYMENT_STATUS = "payment_status"
    SHIPPING_UPDATE = "shipping_update"
    RETURN_STATUS = "return_status"
    REFUND_STATUS = "refund_status"
    REVIEW_RESPONSE = "review_response"
    SYSTEM_ANNOUNCEMENT = "system_announcement"
    PROMOTION = "promotion"
    SECURITY_ALERT = "security_alert"

class NotificationPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class NotificationStatus(enum.Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    priority = Column(Enum(NotificationPriority), default=NotificationPriority.MEDIUM)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.UNREAD)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)  # Additional data specific to notification type
    related_entity_id = Column(UUID(as_uuid=True), nullable=True)  # ID of related entity (order, payment, etc.)
    related_entity_type = Column(String(50), nullable=True)  # Type of related entity
    read_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship('User', backref='notifications')

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'type': self.type.value,
            'priority': self.priority.value,
            'status': self.status.value,
            'title': self.title,
            'message': self.message,
            'data': self.data,
            'related_entity_id': str(self.related_entity_id) if self.related_entity_id else None,
            'related_entity_type': self.related_entity_type,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class NotificationPreference(db.Model):
    __tablename__ = 'notification_preferences'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    email_enabled = Column(Boolean, default=True)
    push_enabled = Column(Boolean, default=True)
    in_app_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship('User', backref='notification_preferences')

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'type': self.type.value,
            'email_enabled': self.email_enabled,
            'push_enabled': self.push_enabled,
            'in_app_enabled': self.in_app_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 