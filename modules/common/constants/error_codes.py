"""



"""

from enum import Enum


class ErrorCode(Enum):
    """
    
    
    HTTP + 2
    40001 = 400Bad Request + 01
    """
    
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
        """
        
        
        Args:
            language:  'zh'
            
        Returns:
            
        """
        messages = {
            'zh': {
                ErrorCode.INVALID_PARAMETER: '',
                ErrorCode.MISSING_PARAMETER: '',
                ErrorCode.INVALID_FORMAT: '',
                ErrorCode.UNAUTHORIZED: '',
                ErrorCode.INVALID_TOKEN: 'Token ',
                ErrorCode.TOKEN_EXPIRED: 'Token ',
                ErrorCode.INVALID_CREDENTIALS: '',
                ErrorCode.FORBIDDEN: '',
                ErrorCode.INSUFFICIENT_PERMISSIONS: '',
                ErrorCode.NOT_FOUND: '',
                ErrorCode.RESOURCE_NOT_FOUND: '',
                ErrorCode.CONFLICT: '',
                ErrorCode.DUPLICATE_ENTRY: '',
                ErrorCode.INTERNAL_ERROR: '',
                ErrorCode.DATABASE_ERROR: '',
                ErrorCode.EXTERNAL_SERVICE_ERROR: '',
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

