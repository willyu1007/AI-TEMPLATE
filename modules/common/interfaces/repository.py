"""
仓储接口定义

提供数据访问层的抽象接口，实现仓储模式。
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from modules.common.models.common import PaginationParams, PaginationResult

T = TypeVar('T')
ID = TypeVar('ID')


class Repository(ABC, Generic[T, ID]):
    """
    基础仓储接口
    
    定义数据访问的基本操作。
    
    Examples:
        >>> class UserRepository(Repository[User, str]):
        ...     def find_by_id(self, id: str) -> Optional[User]:
        ...         # 实现查找逻辑
        ...         pass
    """
    
    @abstractmethod
    def find_by_id(self, id: ID) -> Optional[T]:
        """
        根据 ID 查找实体
        
        Args:
            id: 实体 ID
            
        Returns:
            实体对象，不存在返回 None
        """
        pass
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """
        保存实体（新增或更新）
        
        Args:
            entity: 实体对象
            
        Returns:
            保存后的实体对象
        """
        pass
    
    @abstractmethod
    def delete(self, id: ID) -> bool:
        """
        删除实体
        
        Args:
            id: 实体 ID
            
        Returns:
            删除成功返回 True，否则返回 False
        """
        pass


class CRUDRepository(Repository[T, ID]):
    """
    CRUD 仓储接口
    
    扩展基础仓储接口，提供完整的 CRUD 操作和查询功能。
    """
    
    @abstractmethod
    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        """
        查找所有实体（支持过滤）
        
        Args:
            filters: 过滤条件字典
            
        Returns:
            实体列表
        """
        pass
    
    @abstractmethod
    def find_paginated(
        self,
        params: PaginationParams,
        filters: Optional[Dict[str, Any]] = None
    ) -> PaginationResult[T]:
        """
        分页查找实体
        
        Args:
            params: 分页参数
            filters: 过滤条件字典
            
        Returns:
            分页结果
        """
        pass
    
    @abstractmethod
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        统计实体数量
        
        Args:
            filters: 过滤条件字典
            
        Returns:
            数量
        """
        pass
    
    @abstractmethod
    def exists(self, id: ID) -> bool:
        """
        检查实体是否存在
        
        Args:
            id: 实体 ID
            
        Returns:
            存在返回 True，否则返回 False
        """
        pass

