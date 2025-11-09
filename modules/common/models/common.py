"""
通用数据结构

提供跨模块使用的通用数据结构，如分页、API 响应等。
"""

from typing import Generic, TypeVar, Optional, List, Any
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class PaginationParams:
    """
    分页参数
    
    Attributes:
        page: 页码（从1开始）
        page_size: 每页数量
        max_page_size: 最大每页数量（默认100）
        
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
        """验证和规范化参数"""
        if self.page < 1:
            self.page = 1
        if self.page_size < 1:
            self.page_size = 20
        if self.page_size > self.max_page_size:
            self.page_size = self.max_page_size
    
    def get_offset(self) -> int:
        """
        计算偏移量（用于数据库查询）
        
        Returns:
            偏移量
        """
        return (self.page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """
        获取限制数量
        
        Returns:
            限制数量
        """
        return self.page_size


@dataclass
class PaginationResult(Generic[T]):
    """
    分页结果
    
    Attributes:
        items: 数据列表
        total: 总数量
        page: 当前页码
        page_size: 每页数量
        total_pages: 总页数
        
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
        """计算总页数"""
        if self.total == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size
    
    def has_next(self) -> bool:
        """是否有下一页"""
        return self.page < self.total_pages
    
    def has_prev(self) -> bool:
        """是否有上一页"""
        return self.page > 1


@dataclass
class ApiResponse:
    """
    API 响应结构
    
    Attributes:
        success: 是否成功
        data: 响应数据
        message: 消息
        code: 错误码（失败时）
        
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
    def success_response(cls, data: Any = None, message: str = "操作成功"):
        """创建成功响应"""
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def error_response(cls, message: str, code: int = 400):
        """创建错误响应"""
        return cls(success=False, message=message, code=code)

