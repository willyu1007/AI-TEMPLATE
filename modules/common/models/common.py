"""


API 
"""

from typing import Generic, TypeVar, Optional, List, Any
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class PaginationParams:
    """
    
    
    Attributes:
        page: 1
        page_size: 
        max_page_size: 100
        
    Examples:
        >>> params = PaginationParams(page=1, page_size=20)
        >>> params.page
        1
        >>> params.get_offset()
        0
    """
    page: int = 1
    page_size: int = 20
    max_page_size: int = 100
    
    def __post_init__(self):
        """"""
        if self.page < 1:
            self.page = 1
        if self.page_size < 1:
            self.page_size = 20
        if self.page_size > self.max_page_size:
            self.page_size = self.max_page_size
    
    def get_offset(self) -> int:
        """
        
        
        Returns:
            
        """
        return (self.page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """
        
        
        Returns:
            
        """
        return self.page_size


@dataclass
class PaginationResult(Generic[T]):
    """
    
    
    Attributes:
        items: 
        total: 
        page: 
        page_size: 
        total_pages: 
        
    Examples:
        >>> result = PaginationResult(items=[1, 2, 3], total=10, page=1, page_size=3)
        >>> result.total_pages
        4
        >>> result.has_next()
        True
    """
    items: List[T]
    total: int
    page: int
    page_size: int
    
    @property
    def total_pages(self) -> int:
        """"""
        if self.total == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size
    
    def has_next(self) -> bool:
        """"""
        return self.page < self.total_pages
    
    def has_prev(self) -> bool:
        """"""
        return self.page > 1


@dataclass
class ApiResponse:
    """
    API 
    
    Attributes:
        success: 
        data: 
        message: 
        code: 
        
    Examples:
        >>> response = ApiResponse(success=True, data={"id": "123"})
        >>> response.success
        True
        >>> response = ApiResponse(success=False, message="Error", code=400)
        >>> response.success
        False
    """
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    code: Optional[int] = None
    
    @classmethod
    def success_response(cls, data: Any = None, message: str = ""):
        """"""
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def error_response(cls, message: str, code: int = 400):
        """"""
        return cls(success=False, message=message, code=code)

