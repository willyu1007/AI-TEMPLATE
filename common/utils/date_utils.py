"""
日期时间处理工具函数

提供 UTC 时间、格式化、解析和相对时间等常用功能。
"""

from datetime import datetime, timezone, timedelta
from typing import Optional


def now_utc() -> datetime:
    """
    获取当前 UTC 时间
    
    Returns:
        当前 UTC 时间的 datetime 对象
        
    Examples:
        >>> dt = now_utc()
        >>> isinstance(dt, datetime)
        True
        >>> dt.tzinfo == timezone.utc
        True
    """
    return datetime.now(timezone.utc)


def format_datetime(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    格式化日期时间为字符串
    
    Args:
        dt: datetime 对象
        format_str: 格式字符串（默认 '%Y-%m-%d %H:%M:%S'）
        
    Returns:
        格式化后的字符串
        
    Examples:
        >>> dt = datetime(2025, 11, 5, 10, 30, 0, tzinfo=timezone.utc)
        >>> format_datetime(dt)
        '2025-11-05 10:30:00'
        >>> format_datetime(dt, '%Y-%m-%d')
        '2025-11-05'
    """
    return dt.strftime(format_str)


def parse_datetime(date_string: str, format_str: str = '%Y-%m-%d %H:%M:%S') -> Optional[datetime]:
    """
    解析字符串为 datetime 对象
    
    Args:
        date_string: 日期时间字符串
        format_str: 格式字符串（默认 '%Y-%m-%d %H:%M:%S'）
        
    Returns:
        datetime 对象，解析失败返回 None
        
    Examples:
        >>> dt = parse_datetime('2025-11-05 10:30:00')
        >>> dt.year
        2025
        >>> parse_datetime('invalid') is None
        True
    """
    try:
        return datetime.strptime(date_string, format_str)
    except ValueError:
        return None


def time_ago(dt: datetime, now: Optional[datetime] = None) -> str:
    """
    计算相对时间（如 "5分钟前"、"2小时前"）
    
    Args:
        dt: 目标时间
        now: 当前时间（默认使用当前 UTC 时间）
        
    Returns:
        相对时间描述字符串
        
    Examples:
        >>> past = now_utc() - timedelta(minutes=5)
        >>> time_ago(past)
        '5分钟前'
        >>> past = now_utc() - timedelta(hours=2)
        >>> time_ago(past)
        '2小时前'
    """
    if now is None:
        now = now_utc()
    
    # 确保两个时间都有时区信息
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    
    delta = now - dt
    
    if delta.total_seconds() < 60:
        return f'{int(delta.total_seconds())}秒前'
    elif delta.total_seconds() < 3600:
        return f'{int(delta.total_seconds() / 60)}分钟前'
    elif delta.total_seconds() < 86400:
        return f'{int(delta.total_seconds() / 3600)}小时前'
    elif delta.days < 30:
        return f'{delta.days}天前'
    elif delta.days < 365:
        return f'{delta.days // 30}个月前'
    else:
        return f'{delta.days // 365}年前'

