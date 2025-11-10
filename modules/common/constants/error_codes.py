"""Enumerations for standard API error codes."""

from enum import Enum


class ErrorCode(Enum):
    """HTTP-style error codes (status + suffix, e.g. 40001 = 400 + 01)."""
    
    # 400xx
    INVALID_PARAMETER = 40001
    MISSING_PARAMETER = 40002
    INVALID_FORMAT = 40003
    
    # 401xx
    UNAUTHORIZED = 40101
    INVALID_TOKEN = 40102
    TOKEN_EXPIRED = 40103
    INVALID_CREDENTIALS = 40104
    
    # 403xx
    FORBIDDEN = 40301
    INSUFFICIENT_PERMISSIONS = 40302
    
    # 404xx
    NOT_FOUND = 40401
    RESOURCE_NOT_FOUND = 40402
    
    # 409xx
    CONFLICT = 40901
    DUPLICATE_ENTRY = 40902
    
    # 500xx
    INTERNAL_ERROR = 50001
    DATABASE_ERROR = 50002
    EXTERNAL_SERVICE_ERROR = 50003
    
    def get_message(self, language: str = 'zh') -> str:
        """Return a localized, human-friendly error message."""
        messages = {
            'zh': {
                ErrorCode.INVALID_PARAMETER: '参数无效',
                ErrorCode.MISSING_PARAMETER: '缺少必要参数',
                ErrorCode.INVALID_FORMAT: '格式错误',
                ErrorCode.UNAUTHORIZED: '未授权访问',
                ErrorCode.INVALID_TOKEN: 'Token 无效',
                ErrorCode.TOKEN_EXPIRED: 'Token 已过期',
                ErrorCode.INVALID_CREDENTIALS: '凭证错误',
                ErrorCode.FORBIDDEN: '没有权限',
                ErrorCode.INSUFFICIENT_PERMISSIONS: '权限不足',
                ErrorCode.NOT_FOUND: '资源不存在',
                ErrorCode.RESOURCE_NOT_FOUND: '资源不存在',
                ErrorCode.CONFLICT: '冲突错误',
                ErrorCode.DUPLICATE_ENTRY: '重复数据',
                ErrorCode.INTERNAL_ERROR: '服务器内部错误',
                ErrorCode.DATABASE_ERROR: '数据库错误',
                ErrorCode.EXTERNAL_SERVICE_ERROR: '外部服务错误',
            },
            'en': {
                ErrorCode.INVALID_PARAMETER: 'Invalid parameter',
                ErrorCode.MISSING_PARAMETER: 'Missing required parameter',
                ErrorCode.INVALID_FORMAT: 'Invalid format',
                ErrorCode.UNAUTHORIZED: 'Unauthorized',
                ErrorCode.INVALID_TOKEN: 'Invalid token',
                ErrorCode.TOKEN_EXPIRED: 'Token expired',
                ErrorCode.INVALID_CREDENTIALS: 'Invalid credentials',
                ErrorCode.FORBIDDEN: 'Forbidden',
                ErrorCode.INSUFFICIENT_PERMISSIONS: 'Insufficient permissions',
                ErrorCode.NOT_FOUND: 'Resource not found',
                ErrorCode.RESOURCE_NOT_FOUND: 'Resource not found',
                ErrorCode.CONFLICT: 'Conflict',
                ErrorCode.DUPLICATE_ENTRY: 'Duplicate entry',
                ErrorCode.INTERNAL_ERROR: 'Internal server error',
                ErrorCode.DATABASE_ERROR: 'Database error',
                ErrorCode.EXTERNAL_SERVICE_ERROR: 'External service error',
            }
        }
        return messages.get(language, messages['en']).get(self, 'Unknown error')

