#!/usr/bin/env python3
"""
Trigger Manager - Manage script trigger configurations

Purpose:
- Display all trigger configurations
- Validate trigger-config.yaml
- Query triggers by category/type
- Generate automation coverage report

Usage:
    python scripts/trigger_manager.py show
    python scripts/trigger_manager.py check
    python scripts/trigger_manager.py coverage
    make trigger_show
    make trigger_check
    make trigger_coverage
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class TriggerManager:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = None
        self.errors = []
        
    def load_config(self) -> bool:
        """Load trigger configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            return True
        except Exception as e:
            self.errors.append(f"Failed to load config: {e}")
            return False
            
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.config:
            return False
            
        # Check required fields
        required_top_level = ['version', 'triggers', 'categories']
        for field in required_top_level:
            if field not in self.config:
                self.errors.append(f"Missing required field: {field}")
                
        # Validate triggers
        if 'triggers' in self.config:
            for trigger in self.config['triggers']:
                self._validate_trigger(trigger)
                
        return len(self.errors) == 0
        
    def _validate_trigger(self, trigger: Dict):
        """Validate a single trigger"""
        name = trigger.get('name', '<unnamed>')
        
        # Required fields
        required = ['name', 'script', 'category', 'description', 'triggers', 'commands']
        for field in required:
            if field not in trigger:
                self.errors.append(f"Trigger '{name}': missing field '{field}'")
                
    def show_all(self):
        """Display all triggers"""
        if not self.config:
            print("❌ No config loaded")
            return
            
        triggers = self.config.get('triggers', [])
        categories = {c['id']: c['name'] for c in self.config.get('categories', [])}
        
        print(f"\n📋 Trigger Configuration")
        print(f"   Version: {self.config.get('version')}")
        print(f"   Total Triggers: {len(triggers)}\n")
        
        # Group by category
        by_category = {}
        for trigger in triggers:
            cat = trigger.get('category', 'unknown')
            by_category.setdefault(cat, []).append(trigger)
            
        for cat_id, triggers in sorted(by_category.items()):
            cat_name = categories.get(cat_id, cat_id)
            print(f"## {cat_name} ({len(triggers)})")
            
            for trigger in triggers:
                name = trigger['name']
                desc = trigger['description']
                est_time = trigger.get('estimated_time', 'N/A')
                
                print(f"\n  ✓ {name}")
                print(f"    {desc}")
                print(f"    Time: {est_time}")
                
                # Show trigger types
                trigger_types = trigger.get('triggers', [])
                types_str = ', '.join([t.get('type', 'unknown') for t in trigger_types])
                print(f"    Triggers: {types_str}")
                
                # Show make command
                if 'commands' in trigger and 'make' in trigger['commands']:
                    print(f"    Command: {trigger['commands']['make']}")
                    
            print()
                
    def show_coverage(self):
        """Display automation coverage report"""
        if not self.config:
            print("❌ No config loaded")
            return
            
        coverage = self.config.get('automation_coverage', {})
        
        print("\n📊 Automation Coverage Report\n")
        print(f"Total Scripts: {coverage.get('total_scripts', 0)}")
        print(f"Automated Scripts: {coverage.get('automated_scripts', 0)}")
        print(f"Coverage: {coverage.get('coverage_percentage', 'N/A')}")
        print(f"Target: {coverage.get('target_percentage', 'N/A')}\n")
        
        print("By Category:")
        by_cat = coverage.get('by_category', {})
        for cat, count in by_cat.items():
            print(f"  - {cat}: {count}")
            
        print("\nRecommendations:")
        recs = coverage.get('recommendations', [])
        for rec in recs:
            print(f"  • {rec}")
            
    def report_errors(self):
        """Report validation errors"""
        if self.errors:
            print("\n❌ Validation Errors:\n")
            for error in self.errors:
                print(f"  - {error}")
            return False
        else:
            print("\n✅ Trigger configuration is valid")
            return True


def main():
    """Main entry point"""
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / 'scripts' / 'trigger-config.yaml'
    
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return 1
        
    manager = TriggerManager(config_path)
    
    # Determine command
    command = sys.argv[1] if len(sys.argv) > 1 else 'show'
    
    # Load config
    if not manager.load_config():
        manager.report_errors()
        return 1
        
    # Execute command
    if command == 'show':
        manager.show_all()
    elif command == 'check':
        manager.validate()
        if manager.report_errors():
            return 0
        else:
            return 1
    elif command == 'coverage':
        manager.show_coverage()
    else:
        print(f"Unknown command: {command}")
        print("Usage: trigger_manager.py [show|check|coverage]")
        return 1
        
    return 0


if __name__ == '__main__':
    sys.exit(main())

