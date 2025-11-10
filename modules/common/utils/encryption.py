"""



 bcryptargon2
"""

import hashlib
import base64
from typing import Optional


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """
     SHA-256
    
     bcrypt  argon2
    
    Args:
        password: 
        salt: 
        
    Returns:
        
        
    Examples:
        >>> hashed = hash_password("password123")
        >>> isinstance(hashed, str)
        True
        >>> len(hashed) > 0
        True
    """
    if salt is None:
        salt = "default_salt_change_in_production"
    
    #  SHA-256 
    hash_obj = hashlib.sha256()
    hash_obj.update((password + salt).encode('utf-8'))
    return base64.b64encode(hash_obj.digest()).decode('utf-8')


def verify_password(password: str, hashed_password: str, salt: Optional[str] = None) -> bool:
    """
    
    
    Args:
        password: 
        hashed_password: 
        salt:  hash_password 
        
    Returns:
         True False
        
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
     AES 
    
     cryptography
    
    Args:
        data: 
        key: 
        
    Returns:
         base64 
        
    Examples:
        >>> encrypted = encrypt_data("sensitive_data")
        >>> isinstance(encrypted, str)
        True
    """
    if key is None:
        key = "default_key_change_in_production"
    
    #  XOR 
    encrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
    return base64.b64encode(encrypted.encode('utf-8')).decode('utf-8')


def decrypt_data(encrypted_data: str, key: Optional[str] = None) -> str:
    """
    
    
    Args:
        encrypted_data:  base64 
        key: 
        
    Returns:
        
        
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

