import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, Boolean, ForeignKey, Enum, CheckConstraint, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import db, BaseModel
import enum

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

class Notification(BaseModel):
    """Notification model for user notifications."""
    __tablename__ = 'notifications'
    __table_args__ = {'extend_existing': True}
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.Enum(NotificationType), nullable=False)
    priority = db.Column(db.Enum(NotificationPriority), default=NotificationPriority.MEDIUM)
    status = db.Column(db.Enum(NotificationStatus), default=NotificationStatus.UNREAD)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    data = db.Column(db.JSON, nullable=True)  # Additional data specific to notification type
    related_entity_id = db.Column(db.String(36), nullable=True)  # ID of related entity (order, payment, etc.)
    related_entity_type = db.Column(db.String(50), nullable=True)  # Type of related entity
    read_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    
    def to_dict(self):
        """Convert notification instance to dictionary."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'type': self.type.value if self.type else None,
            'priority': self.priority.value if self.priority else None,
            'status': self.status.value if self.status else None,
            'title': self.title,
            'message': self.message,
            'data': self.data,
            'related_entity_id': self.related_entity_id,
            'related_entity_type': self.related_entity_type,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        })
        return data

class NotificationPreference(BaseModel):
    """Model for user notification preferences."""
    __tablename__ = 'notification_preferences'
    __table_args__ = {'extend_existing': True}
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.Enum(NotificationType), nullable=False)
    email_enabled = db.Column(db.Boolean, default=True)
    push_enabled = db.Column(db.Boolean, default=True)
    in_app_enabled = db.Column(db.Boolean, default=True)
    
    # Relationships
    user = db.relationship('User', backref='notification_preferences')
    
    def to_dict(self):
        """Convert notification preference instance to dictionary."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'type': self.type.value if self.type else None,
            'email_enabled': self.email_enabled,
            'push_enabled': self.push_enabled,
            'in_app_enabled': self.in_app_enabled
        })
        return data 