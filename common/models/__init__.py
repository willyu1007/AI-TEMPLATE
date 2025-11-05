"""
共享数据模型模块

提供跨模块使用的基础模型类和通用数据结构。
"""

from .base import BaseModel, TimestampMixin
from .common import (
    PaginationParams,
    PaginationResult,
    ApiResponse,
)

__all__ = [
    'BaseModel',
    'TimestampMixin',
    'PaginationParams',
    'PaginationResult',
    'ApiResponse',
]

