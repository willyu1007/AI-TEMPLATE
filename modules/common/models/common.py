"""Common pagination and response models shared by APIs."""

from typing import Generic, TypeVar, Optional, List, Any
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class PaginationParams:
    """Pagination parameters with guards for page/page_size/max limits."""
    page: int = 1
    page_size: int = 20
    max_page_size: int = 100
    
    def __post_init__(self):
        """Clamp page/page_size so they stay within valid ranges."""
        if self.page < 1:
            self.page = 1
        if self.page_size < 1:
            self.page_size = 20
        if self.page_size > self.max_page_size:
            self.page_size = self.max_page_size
    
    def get_offset(self) -> int:
        """Return the zero-based offset for queries."""
        return (self.page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """Return the page_size to be used in queries."""
        return self.page_size


@dataclass
class PaginationResult(Generic[T]):
    """Wrapper for paginated results with helper methods."""
    items: List[T]
    total: int
    page: int
    page_size: int
    
    @property
    def total_pages(self) -> int:
        """Return how many pages are available."""
        if self.total == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size
    
    def has_next(self) -> bool:
        """Return True when there is a next page."""
        return self.page < self.total_pages
    
    def has_prev(self) -> bool:
        """Return True when there is a previous page."""
        return self.page > 1


@dataclass
class ApiResponse:
    """Simple API response envelope."""
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    code: Optional[int] = None
    
    @classmethod
    def success_response(cls, data: Any = None, message: str = ""):
        """Factory for a successful response."""
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def error_response(cls, message: str, code: int = 400):
        """Factory for an error response."""
        return cls(success=False, message=message, code=code)

