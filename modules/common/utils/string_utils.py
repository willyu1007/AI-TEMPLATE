"""String helper utilities."""

import re
from typing import Optional


def camel_to_snake(name: str) -> str:
    """Convert CamelCase or mixedCase names to snake_case."""
    # First, split `UserProfile` -> `User_Profile`
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(name: str, capitalize_first: bool = False) -> str:
    """Convert snake_case to camelCase or PascalCase."""
    components = name.split('_')
    if capitalize_first:
        return ''.join(word.capitalize() for word in components)
    else:
        return components[0] + ''.join(word.capitalize() for word in components[1:])


def truncate_string(s: str, max_length: int, suffix: str = '...') -> str:
    """Truncate a string and append the suffix when it exceeds `max_length`."""
    if len(s) <= max_length:
        return s
    return s[:max_length] + suffix


def normalize_string(s: str, trim: bool = True, lower: bool = False) -> str:
    """Trim whitespace and optionally lowercase the provided string."""
    result = s
    if trim:
        result = result.strip()
    if lower:
        result = result.lower()
    return result

