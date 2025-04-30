import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import db

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default='pending')  # pending, completed, cancelled
    payment_method = Column(String(50), nullable=True)
    shipping_address = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="transactions")
    items = relationship("TransactionItem", back_populates="transaction", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'total_amount': self.total_amount,
            'status': self.status,
            'payment_method': self.payment_method,
            'shipping_address': self.shipping_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items] if self.items else []
        }


class TransactionItem(db.Model):
    __tablename__ = 'transaction_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey('transactions.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)  # Price at time of purchase
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="items")
    product = relationship("Product")
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'transaction_id': str(self.transaction_id),
            'product_id': str(self.product_id),
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.price * self.quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 