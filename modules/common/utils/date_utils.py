"""Date/time helpers used across modules."""

from datetime import datetime, timezone, timedelta
from typing import Optional


def now_utc() -> datetime:
    """Return the current UTC timestamp with timezone info."""
    return datetime.now(timezone.utc)


def format_datetime(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """Format a datetime using the provided format string."""
    return dt.strftime(format_str)


def parse_datetime(date_string: str, format_str: str = '%Y-%m-%d %H:%M:%S') -> Optional[datetime]:
    """Parse a datetime string. Returns None when parsing fails."""
    try:
        return datetime.strptime(date_string, format_str)
    except ValueError:
        return None


def time_ago(dt: datetime, now: Optional[datetime] = None) -> str:
    """Return a coarse relative time (seconds/minutes/hours/days/months/years)."""
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

