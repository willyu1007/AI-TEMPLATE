"""Validation helpers for email/phone/URL/UUID strings."""

import re
import uuid
from typing import Optional


def validate_email(email: str) -> bool:
    """Return True if the string looks like a valid email address."""
    if not email or not isinstance(email, str):
        return False
    
    # 
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str, country_code: str = 'CN') -> bool:
    """Validate a phone number. Defaults to mainland China format, falls back to simple digit check."""
    if not phone or not isinstance(phone, str):
        return False
    
    # 
    phone = phone.replace(' ', '').replace('-', '')
    
    if country_code == 'CN':
        # Mainland China mobile numbers start with 1[3-9] and have 11 digits
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone))
    else:
        # Basic validation for other countries
        return phone.isdigit() and len(phone) >= 10


def validate_url(url: str) -> bool:
    """Return True when the string starts with http(s):// and matches a basic URL pattern."""
    if not url or not isinstance(url, str):
        return False
    
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def validate_uuid(uuid_string: str) -> bool:
    """Return True if the string is a valid UUID (any version)."""
    if not uuid_string or not isinstance(uuid_string, str):
        return False
    
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False

