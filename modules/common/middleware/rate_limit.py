"""Simple in-memory rate limiter utilities."""

import time
from typing import Dict, Tuple, Optional, Callable, Any
from collections import defaultdict
from functools import wraps


class RateLimiter:
    """Track requests per identifier within a sliding window."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """Initialize a limiter with the given quota and window size."""
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> Tuple[bool, int]:
        """Return (allowed, remaining) for the provided identifier."""
        now = time.time()
        window_start = now - self.window_seconds
        
        # 
        self.requests[identifier] = [
            ts for ts in self.requests[identifier]
            if ts > window_start
        ]
        
        # 
        if len(self.requests[identifier]) >= self.max_requests:
            remaining = 0
        else:
            self.requests[identifier].append(now)
            remaining = self.max_requests - len(self.requests[identifier])
        
        allowed = len(self.requests[identifier]) <= self.max_requests
        return allowed, remaining


# 
_default_limiter = RateLimiter(max_requests=100, window_seconds=60)


def rate_limit(
    max_requests: int = 100,
    window_seconds: int = 60,
    identifier_func: Optional[Callable[..., str]] = None
):
    """Decorator factory that enforces RateLimiter on a function."""
    limiter = RateLimiter(max_requests, window_seconds)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 
            if identifier_func:
                identifier = identifier_func(*args, **kwargs)
            else:
                identifier = func.__name__
            
            allowed, remaining = limiter.is_allowed(identifier)
            if not allowed:
                raise Exception(f"Rate limit exceeded. Remaining: {remaining}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

