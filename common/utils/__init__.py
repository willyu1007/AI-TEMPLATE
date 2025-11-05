"""
通用工具函数模块

提供跨模块共享的工具函数，包括字符串处理、日期时间、数据验证和加密解密等功能。
"""

from .string_utils import (
    camel_to_snake,
    snake_to_camel,
    truncate_string,
    normalize_string,
)
from .date_utils import (
    now_utc,
    format_datetime,
    parse_datetime,
    time_ago,
)
from .validation import (
    validate_email,
    validate_phone,
    validate_url,
    validate_uuid,
)
from .encryption import (
    hash_password,
    verify_password,
    encrypt_data,
    decrypt_data,
)

__all__ = [
    # 字符串工具
    'camel_to_snake',
    'snake_to_camel',
    'truncate_string',
    'normalize_string',
    # 日期时间工具
    'now_utc',
    'format_datetime',
    'parse_datetime',
    'time_ago',
    # 验证工具
    'validate_email',
    'validate_phone',
    'validate_url',
    'validate_uuid',
    # 加密工具
    'hash_password',
    'verify_password',
    'encrypt_data',
    'decrypt_data',
]

