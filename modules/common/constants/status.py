"""Common status enums shared by modules."""

from enum import Enum


class Status(Enum):
    """Generic lifecycle status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"


class UserStatus(Enum):
    """User-specific status values."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BANNED = "banned"
    PENDING_VERIFICATION = "pending_verification"


class OrderStatus(Enum):
    """Order state transitions."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

