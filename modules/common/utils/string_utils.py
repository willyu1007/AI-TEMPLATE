"""



"""

import re
from typing import Optional


def camel_to_snake(name: str) -> str:
    """
    
    
    Args:
        name:  "UserProfile"
        
    Returns:
         "user_profile"
        
    Examples:
        >>> camel_to_snake("UserProfile")
        'user_profile'
        >>> camel_to_snake("HTTPRequest")
        'http_request'
    """
    # 
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(name: str, capitalize_first: bool = False) -> str:
    """
    
    
    Args:
        name:  "user_profile"
        capitalize_first:  False
        
    Returns:
        
        
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
    
    
    Args:
        s: 
        max_length: 
        suffix:  "..."
        
    Returns:
        
        
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
    
    
    Args:
        s: 
        trim:  True
        lower:  False
        
    Returns:
        
        
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

