"""


URLUUID 
"""

import re
import uuid
from typing import Optional


def validate_email(email: str) -> bool:
    """
    
    
    Args:
        email: 
        
    Returns:
         True False
        
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
    
    # 
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str, country_code: str = 'CN') -> bool:
    """
    
    
    Args:
        phone: 
        country_code:  'CN' 
        
    Returns:
         True False
        
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
    
    # 
    phone = phone.replace(' ', '').replace('-', '')
    
    if country_code == 'CN':
        # 111
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone))
    else:
        # 
        # 
        return phone.isdigit() and len(phone) >= 10


def validate_url(url: str) -> bool:
    """
     URL 
    
    Args:
        url: URL 
        
    Returns:
         True False
        
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
     UUID 
    
    Args:
        uuid_string: UUID 
        
    Returns:
         True False
        
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

