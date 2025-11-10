"""



"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from modules.common.models.common import PaginationParams, PaginationResult

T = TypeVar('T')
ID = TypeVar('ID')


class Repository(ABC, Generic[T, ID]):
    """
    
    
    
    
    Examples:
        >>> class UserRepository(Repository[User, str]):
        ...     def find_by_id(self, id: str) -> Optional[User]:
        ...         # 
        ...         pass
    """
    
    @abstractmethod
    def find_by_id(self, id: ID) -> Optional[T]:
        """
         ID 
        
        Args:
            id:  ID
            
        Returns:
             None
        """
        pass
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """
        
        
        Args:
            entity: 
            
        Returns:
            
        """
        pass
    
    @abstractmethod
    def delete(self, id: ID) -> bool:
        """
        
        
        Args:
            id:  ID
            
        Returns:
             True False
        """
        pass


class CRUDRepository(Repository[T, ID]):
    """
    CRUD 
    
     CRUD 
    """
    
    @abstractmethod
    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        """
        
        
        Args:
            filters: 
            
        Returns:
            
        """
        pass
    
    @abstractmethod
    def find_paginated(
        self,
        params: PaginationParams,
        filters: Optional[Dict[str, Any]] = None
    ) -> PaginationResult[T]:
        """
        
        
        Args:
            params: 
            filters: 
            
        Returns:
            
        """
        pass
    
    @abstractmethod
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        
        
        Args:
            filters: 
            
        Returns:
            
        """
        pass
    
    @abstractmethod
    def exists(self, id: ID) -> bool:
        """
        
        
        Args:
            id:  ID
            
        Returns:
             True False
        """
        pass

