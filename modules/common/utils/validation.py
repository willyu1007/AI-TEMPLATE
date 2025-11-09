"""
数据验证工具函数

提供常用的数据验证功能，包括邮箱、手机号、URL、UUID 等验证。
"""

import re
import uuid
from typing import Optional


def validate_email(email: str) -> bool:
    """
    验证邮箱地址格式
    
    Args:
        email: 邮箱地址字符串
        
    Returns:
        验证通过返回 True，否则返回 False
        
    Examples:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid.email")
        False
        >>> validate_email("")
        False
    """
    if not email or not isinstance(email, str):
        return False
    
    # 简化的邮箱正则表达式
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str, country_code: str = 'CN') -> bool:
    """
    验证手机号格式
    
    Args:
        phone: 手机号字符串
        country_code: 国家代码（默认 'CN' 中国）
        
    Returns:
        验证通过返回 True，否则返回 False
        
    Examples:
        >>> validate_phone("13800138000")
        True
        >>> validate_phone("1234567890")
        False
        >>> validate_phone("")
        False
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # 移除可能的空格和连字符
    phone = phone.replace(' ', '').replace('-', '')
    
    if country_code == 'CN':
        # 中国手机号：11位数字，以1开头
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone))
    else:
        # 其他国家的验证逻辑可以扩展
        # 目前只验证是否为数字
        return phone.isdigit() and len(phone) >= 10


def validate_url(url: str) -> bool:
    """
    验证 URL 格式
    
    Args:
        url: URL 字符串
        
    Returns:
        验证通过返回 True，否则返回 False
        
    Examples:
        >>> validate_url("https://example.com")
        True
        >>> validate_url("http://localhost:8000/api")
        True
        >>> validate_url("not-a-url")
        False
    """
    if not url or not isinstance(url, str):
        return False
    
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def validate_uuid(uuid_string: str) -> bool:
    """
    验证 UUID 格式
    
    Args:
        uuid_string: UUID 字符串
        
    Returns:
        验证通过返回 True，否则返回 False
        
    Examples:
        >>> validate_uuid("123e4567-e89b-12d3-a456-426614174000")
        True
        >>> validate_uuid("invalid-uuid")
        False
        >>> validate_uuid("")
        False
    """
    if not uuid_string or not isinstance(uuid_string, str):
        return False
    
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False

