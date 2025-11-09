"""
限流中间件

提供基于时间窗口的请求限流功能。
"""

import time
from typing import Dict, Tuple, Optional, Callable, Any
from collections import defaultdict
from functools import wraps


class RateLimiter:
    """
    限流器
    
    基于滑动时间窗口实现限流。
    
    Attributes:
        max_requests: 时间窗口内最大请求数
        window_seconds: 时间窗口大小（秒）
        
    Examples:
        >>> limiter = RateLimiter(max_requests=10, window_seconds=60)
        >>> limiter.is_allowed("user123")
        True
    """
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        初始化限流器
        
        Args:
            max_requests: 时间窗口内最大请求数
            window_seconds: 时间窗口大小（秒）
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> Tuple[bool, int]:
        """
        检查是否允许请求
        
        Args:
            identifier: 请求标识符（如用户ID、IP地址等）
            
        Returns:
            (是否允许, 剩余请求数)
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        # 清理过期请求
        self.requests[identifier] = [
            ts for ts in self.requests[identifier]
            if ts > window_start
        ]
        
        # 检查是否超过限制
        if len(self.requests[identifier]) >= self.max_requests:
            remaining = 0
        else:
            self.requests[identifier].append(now)
            remaining = self.max_requests - len(self.requests[identifier])
        
        allowed = len(self.requests[identifier]) <= self.max_requests
        return allowed, remaining


# 全局限流器实例
_default_limiter = RateLimiter(max_requests=100, window_seconds=60)


def rate_limit(
    max_requests: int = 100,
    window_seconds: int = 60,
    identifier_func: Optional[Callable[..., str]] = None
):
    """
    限流装饰器
    
    Args:
        max_requests: 时间窗口内最大请求数
        window_seconds: 时间窗口大小（秒）
        identifier_func: 获取请求标识符的函数（可选）
        
    Returns:
        装饰后的函数
        
    Examples:
        >>> @rate_limit(max_requests=10, window_seconds=60)
        ... def api_endpoint():
        ...     return "response"
    """
    limiter = RateLimiter(max_requests, window_seconds)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取标识符（默认使用函数名）
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

