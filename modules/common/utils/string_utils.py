"""
字符串处理工具函数

提供常用的字符串操作功能，包括命名转换、截断、规范化等。
"""

import re
from typing import Optional


def camel_to_snake(name: str) -> str:
    """
    将驼峰命名转换为蛇形命名
    
    Args:
        name: 驼峰命名字符串（如 "UserProfile"）
        
    Returns:
        蛇形命名字符串（如 "user_profile"）
        
    Examples:
        >>> camel_to_snake("UserProfile")
        'user_profile'
        >>> camel_to_snake("HTTPRequest")
        'http_request'
    """
    # 在大写字母前插入下划线，然后转小写
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(name: str, capitalize_first: bool = False) -> str:
    """
    将蛇形命名转换为驼峰命名
    
    Args:
        name: 蛇形命名字符串（如 "user_profile"）
        capitalize_first: 是否首字母大写（默认 False）
        
    Returns:
        驼峰命名字符串
        
    Examples:
        >>> snake_to_camel("user_profile")
        'userProfile'
        >>> snake_to_camel("user_profile", capitalize_first=True)
        'UserProfile'
    """
    components = name.split('_')
    if capitalize_first:
        return ''.join(word.capitalize() for word in components)
    else:
        return components[0] + ''.join(word.capitalize() for word in components[1:])


def truncate_string(s: str, max_length: int, suffix: str = '...') -> str:
    """
    截断字符串，超过最大长度时添加后缀
    
    Args:
        s: 原始字符串
        max_length: 最大长度（不含后缀）
        suffix: 截断后的后缀（默认 "..."）
        
    Returns:
        截断后的字符串
        
    Examples:
        >>> truncate_string("Hello World", 5)
        'Hello...'
        >>> truncate_string("Hello", 10)
        'Hello'
    """
    if len(s) <= max_length:
        return s
    return s[:max_length] + suffix


def normalize_string(s: str, trim: bool = True, lower: bool = False) -> str:
    """
    规范化字符串（去除空白、统一格式等）
    
    Args:
        s: 原始字符串
        trim: 是否去除首尾空白（默认 True）
        lower: 是否转为小写（默认 False）
        
    Returns:
        规范化后的字符串
        
    Examples:
        >>> normalize_string("  Hello World  ", trim=True)
        'Hello World'
        >>> normalize_string("Hello World", lower=True)
        'hello world'
    """
    result = s
    if trim:
        result = result.strip()
    if lower:
        result = result.lower()
    return result

