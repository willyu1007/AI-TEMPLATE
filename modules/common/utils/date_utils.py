"""


 UTC 
"""

from datetime import datetime, timezone, timedelta
from typing import Optional


def now_utc() -> datetime:
    """
     UTC 
    
    Returns:
         UTC  datetime 
        
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
    
    
    Args:
        dt: datetime 
        format_str:  '%Y-%m-%d %H:%M:%S'
        
    Returns:
        
        
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
     datetime 
    
    Args:
        date_string: 
        format_str:  '%Y-%m-%d %H:%M:%S'
        
    Returns:
        datetime  None
        
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
     "5""2"
    
    Args:
        dt: 
        now:  UTC 
        
    Returns:
        
        
    Examples:
        >>> past = now_utc() - timedelta(minutes=5)
        >>> time_ago(past)
        '5'
        >>> past = now_utc() - timedelta(hours=2)
        >>> time_ago(past)
        '2'
    """
    if now is None:
        now = now_utc()
    
    # 
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    
    delta = now - dt
    
    if delta.total_seconds() < 60:
        return f'{int(delta.total_seconds())}'
    elif delta.total_seconds() < 3600:
        return f'{int(delta.total_seconds() / 60)}'
    elif delta.total_seconds() < 86400:
        return f'{int(delta.total_seconds() / 3600)}'
    elif delta.days < 30:
        return f'{delta.days}'
    elif delta.days < 365:
        return f'{delta.days // 30}'
    else:
        return f'{delta.days // 365}'

