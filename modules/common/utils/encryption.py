"""
加密解密工具函数

提供密码哈希、验证和数据加密解密功能。
注意：实际项目中应使用更安全的加密库（如 bcrypt、argon2）。
"""

import hashlib
import base64
from typing import Optional


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """
    哈希密码（使用 SHA-256）
    
    警告：此函数仅作为示例，生产环境应使用 bcrypt 或 argon2。
    
    Args:
        password: 原始密码
        salt: 盐值（可选，默认使用固定盐）
        
    Returns:
        哈希后的密码字符串
        
    Examples:
        >>> hashed = hash_password("password123")
        >>> isinstance(hashed, str)
        True
        >>> len(hashed) > 0
        True
    """
    if salt is None:
        salt = "default_salt_change_in_production"
    
    # 使用 SHA-256 哈希
    hash_obj = hashlib.sha256()
    hash_obj.update((password + salt).encode('utf-8'))
    return base64.b64encode(hash_obj.digest()).decode('utf-8')


def verify_password(password: str, hashed_password: str, salt: Optional[str] = None) -> bool:
    """
    验证密码是否匹配哈希值
    
    Args:
        password: 原始密码
        hashed_password: 哈希后的密码
        salt: 盐值（必须与 hash_password 时使用的相同）
        
    Returns:
        匹配返回 True，否则返回 False
        
    Examples:
        >>> hashed = hash_password("password123")
        >>> verify_password("password123", hashed)
        True
        >>> verify_password("wrong_password", hashed)
        False
    """
    return hash_password(password, salt) == hashed_password


def encrypt_data(data: str, key: Optional[str] = None) -> str:
    """
    加密数据（简单示例，实际应使用 AES 等加密算法）
    
    警告：此函数仅作为示例，生产环境应使用专业的加密库（如 cryptography）。
    
    Args:
        data: 要加密的字符串
        key: 加密密钥（可选）
        
    Returns:
        加密后的 base64 编码字符串
        
    Examples:
        >>> encrypted = encrypt_data("sensitive_data")
        >>> isinstance(encrypted, str)
        True
    """
    if key is None:
        key = "default_key_change_in_production"
    
    # 简单的 XOR 加密（仅示例，不用于生产）
    encrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
    return base64.b64encode(encrypted.encode('utf-8')).decode('utf-8')


def decrypt_data(encrypted_data: str, key: Optional[str] = None) -> str:
    """
    解密数据
    
    Args:
        encrypted_data: 加密后的 base64 编码字符串
        key: 解密密钥（必须与加密时使用的相同）
        
    Returns:
        解密后的原始字符串
        
    Examples:
        >>> encrypted = encrypt_data("sensitive_data")
        >>> decrypt_data(encrypted)
        'sensitive_data'
    """
    if key is None:
        key = "default_key_change_in_production"
    
    try:
        decoded = base64.b64decode(encrypted_data).decode('utf-8')
        decrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(decoded))
        return decrypted
    except Exception:
        return ""

