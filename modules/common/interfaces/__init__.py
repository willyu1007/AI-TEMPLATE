"""
共享接口定义模块

提供跨模块使用的接口定义，如仓储模式接口等。
"""

from .repository import Repository, CRUDRepository

__all__ = [
    'Repository',
    'CRUDRepository',
]

