"""
全局常量模块

提供错误码、状态常量等全局定义。
"""

from .error_codes import ErrorCode
from .status import Status, UserStatus, OrderStatus

__all__ = [
    'ErrorCode',
    'Status',
    'UserStatus',
    'OrderStatus',
]

