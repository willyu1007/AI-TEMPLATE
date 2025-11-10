"""Base dataclasses and mixins for module models."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from dataclasses import dataclass, field, asdict


@dataclass
class BaseModel:
    """Lightweight base model with helpers for dict/JSON conversion."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Return a shallow dictionary representation."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Serialize the model to JSON using default=str."""
        import json
        return json.dumps(self.to_dict(), default=str, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Instantiate the dataclass from a dict."""
        return cls(**data)


@dataclass
class TimestampMixin:
    """Mixin that automatically tracks `created_at` and `updated_at`."""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    
    def touch(self):
        """Update the `updated_at` timestamp to now."""
        self.updated_at = datetime.now(timezone.utc)

