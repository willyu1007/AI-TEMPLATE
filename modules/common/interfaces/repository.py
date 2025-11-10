"""Repository interfaces shared by Module implementations."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from modules.common.models.common import PaginationParams, PaginationResult

T = TypeVar('T')
ID = TypeVar('ID')


class Repository(ABC, Generic[T, ID]):
    """Base repository contract for modules that persist domain objects."""
    
    @abstractmethod
    def find_by_id(self, id: ID) -> Optional[T]:
        """Return the entity with the given identifier or None if it does not exist."""
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """Create or update an entity and return the stored version."""
    
    @abstractmethod
    def delete(self, id: ID) -> bool:
        """Remove an entity by id. Returns True if one row was removed."""


class CRUDRepository(Repository[T, ID]):
    """Extended repository contract that adds bulk and pagination helpers."""
    
    @abstractmethod
    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        """Return all entities that match the optional filter criteria."""
    
    @abstractmethod
    def find_paginated(
        self,
        params: PaginationParams,
        filters: Optional[Dict[str, Any]] = None
    ) -> PaginationResult[T]:
        """Return a paginated result set honoring the provided filters."""
    
    @abstractmethod
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Return how many entities satisfy the filters."""
    
    @abstractmethod
    def exists(self, id: ID) -> bool:
        """Return True when an entity with the given id exists."""

