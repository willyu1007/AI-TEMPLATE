"""
状态常量定义

提供常用的状态枚举，如通用状态、用户状态、订单状态等。
"""

from enum import Enum


class Status(Enum):
    """
    通用状态枚举
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"


class UserStatus(Enum):
    """
    用户状态枚举
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BANNED = "banned"
    PENDING_VERIFICATION = "pending_verification"


class OrderStatus(Enum):
    """
    订单状态枚举
    """
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

