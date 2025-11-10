#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
issue_model.py - Standardized Issue Object Model for Health Checks

This module defines the standard Issue object used across all health check tools.
Provides precise problem location (file/line/context) and fix suggestions.

Created: 2025-11-09 (Phase 14.2+)
"""

import sys
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class IssueLevel(Enum):
    """Issue severity levels"""
    BLOCKER = "blocker"      # Must fix immediately - blocks release
    ERROR = "error"          # Must fix - high priority
    WARNING = "warning"      # Should fix - medium priority
    INFO = "info"           # Informational - low priority
    SUGGESTION = "suggestion"  # Optional improvement


class IssueCategory(Enum):
    """Issue categories matching health dimensions"""
    CODE_QUALITY = "code_quality"
    DOCUMENTATION = "documentation"
    ARCHITECTURE = "architecture"
    AI_FRIENDLINESS = "ai_friendliness"
    OPERATIONS = "operations"
    SECURITY = "security"


@dataclass
class Issue:
    """
    Standardized issue object for precise problem reporting
    
    Provides:
    - Precise location (file, line, column)
    - Code context (before/after lines)
    - Fix suggestions with commands
    - Priority for sorting
    """
    
    # Basic information
    level: IssueLevel           # Issue severity level
    category: IssueCategory     # Issue category
    rule: str                   # Rule ID (e.g., "DOC-001", "BLOCKER-002")
    message: str                # Problem description
    
    # Location information
    file: Optional[str] = None       # File path
    line: Optional[int] = None       # Line number
    column: Optional[int] = None     # Column number
    context_before: List[str] = field(default_factory=list)  # 3 lines before
    context_after: List[str] = field(default_factory=list)   # 3 lines after
    
    # Fix suggestions
    suggestion: Optional[str] = None         # Fix suggestion text
    fix_command: Optional[str] = None        # Command to fix
    reference: Optional[str] = None          # Reference document path
    estimated_time: Optional[str] = None     # Estimated fix time
    
    # Priority (0-100, higher = more urgent)
    priority: int = 50
    
    # Additional metadata
    impact: Optional[str] = None  # Impact description
    tags: List[str] = field(default_factory=list)  # Additional tags
    
    def __post_init__(self):
        """Validate issue object after initialization"""
        if not isinstance(self.level, IssueLevel):
            raise ValueError(f"level must be IssueLevel enum, got {type(self.level)}")
        if not isinstance(self.category, IssueCategory):
            raise ValueError(f"category must be IssueCategory enum, got {type(self.category)}")
        if not self.rule:
            raise ValueError("rule is required")
        if not self.message:
            raise ValueError("message is required")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert issue to dictionary for JSON serialization
        
        Returns:
            Dict with all issue data (enums converted to strings)
        """
        data = asdict(self)
        data['level'] = self.level.value
        data['category'] = self.category.value
        return data
    
    def to_markdown(self, include_context: bool = True) -> str:
        """
        Convert issue to Markdown format
        
        Args:
            include_context: Whether to include code context
            
        Returns:
            Markdown formatted issue description
        """
        # Emoji mapping
        level_emoji = {
            IssueLevel.BLOCKER: "🔥",
            IssueLevel.ERROR: "❌",
            IssueLevel.WARNING: "⚠️",
            IssueLevel.INFO: "ℹ️",
            IssueLevel.SUGGESTION: "💡"
        }
        
        md = f"{level_emoji.get(self.level, '•')} **[{self.rule}]** {self.message}\n\n"
        
        # Location
        if self.file:
            md += f"- ****: `{self.file}`"
            if self.line:
                md += f":{self.line}"
                if self.column:
                    md += f":{self.column}"
            md += "\n"
        
        # Code context
        if include_context and (self.context_before or self.context_after):
            md += "- ****:\n\n```python\n"
            if self.context_before:
                for line in self.context_before:
                    md += f"{line}\n"
            md += ">>> ISSUE LINE <<<\n"  # Marker for issue line
            if self.context_after:
                for line in self.context_after:
                    md += f"{line}\n"
            md += "```\n\n"
        
        # Fix information
        if self.suggestion:
            md += f"- ****: {self.suggestion}\n"
        if self.fix_command:
            md += f"- ****: `{self.fix_command}`\n"
        if self.estimated_time:
            md += f"- ****: {self.estimated_time}\n"
        if self.reference:
            md += f"- ****: {self.reference}\n"
        if self.impact:
            md += f"- ****: {self.impact}\n"
        
        # Tags
        if self.tags:
            md += f"- ****: {', '.join(self.tags)}\n"
        
        return md
    
    def get_location_string(self) -> str:
        """
        Get human-readable location string
        
        Returns:
            Location string like "file.py:123" or "unknown"
        """
        if not self.file:
            return "unknown"
        location = self.file
        if self.line:
            location += f":{self.line}"
            if self.column:
                location += f":{self.column}"
        return location
    
    def is_blocker(self) -> bool:
        """Check if this is a blocker issue"""
        return self.level == IssueLevel.BLOCKER or self.rule.startswith('BLOCKER-')
    
    def is_high_priority(self) -> bool:
        """Check if this is high priority (blocker or error)"""
        return self.level in [IssueLevel.BLOCKER, IssueLevel.ERROR]


def create_issue(
    level: str,
    category: str,
    rule: str,
    message: str,
    **kwargs
) -> Issue:
    """
    Convenience function to create Issue with string enums
    
    Args:
        level: Level string ("blocker", "error", "warning", "info", "suggestion")
        category: Category string ("code_quality", "documentation", etc.)
        rule: Rule ID
        message: Problem description
        **kwargs: Additional Issue fields
        
    Returns:
        Issue object
    """
    level_enum = IssueLevel(level)
    category_enum = IssueCategory(category)
    return Issue(
        level=level_enum,
        category=category_enum,
        rule=rule,
        message=message,
        **kwargs
    )


# Example usage and testing
if __name__ == '__main__':
    # Test Issue creation
    issue1 = create_issue(
        level="error",
        category="code_quality",
        rule="CQ-001",
        message="Linter check failed: unused import 'os'",
        file="scripts/example.py",
        line=10,
        column=1,
        context_before=["import sys", "import json", ""],
        context_after=["", "def main():", "    pass"],
        suggestion="Remove unused import or use it",
        fix_command="make python_scripts_lint --fix",
        reference="/doc/process/AI_CODING_GUIDE.md",
        estimated_time="2 minutes",
        priority=80
    )
    
    print("=== Issue Object Test ===\n")
    print(f"Location: {issue1.get_location_string()}")
    print(f"Is blocker: {issue1.is_blocker()}")
    print(f"Is high priority: {issue1.is_high_priority()}\n")
    
    print("=== Markdown Format ===\n")
    print(issue1.to_markdown())
    
    print("\n=== JSON Format ===\n")
    import json
    print(json.dumps(issue1.to_dict(), indent=2, ensure_ascii=False))
    
    print("\n✅ Issue model test completed successfully!")

