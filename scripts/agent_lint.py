#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent_lint.py - agent.md YAMLLint


1. agent.md
2. YAML Front Matter
3. 
4. schemas/agent.schema.yamlSchemajsonschema
5. context_routes
6. trigger_config


    python scripts/agent_lint.py
    python scripts/agent_lint.py --json
    python scripts/agent_lint.py --markdown
    make agent_lint
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any

# Lint
from base_lint import BaseLinter, LintIssue, Severity, run_linter

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "agent.schema.yaml"

# YAML Front Matter
YAML_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


class AgentLinter(BaseLinter):
    """agent.md"""
    
    @property
    def name(self) -> str:
        """Linter"""
        return "Agent"
    
    def __init__(self, repo_root: Optional[Path] = None):
        """"""
        super().__init__(repo_root)
        self.schema = self._load_schema()
        self.has_jsonschema = self._check_jsonschema()
        self.required_fields = ["spec_version", "agent_id", "role"]
        self.trigger_rules = self._load_trigger_rules()
    
    def _load_schema(self) -> Optional[Dict[str, Any]]:
        """agent.schema.yaml"""
        if not SCHEMA_PATH.exists():
            return None
        try:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[warn] Schema: {e}", file=sys.stderr)
            return None
    
    def _check_jsonschema(self) -> bool:
        """jsonschema"""
        try:
            import jsonschema
            return True
        except ImportError:
            return False
    
    def _load_trigger_rules(self) -> Optional[set]:
        """agent-triggers.yamlID"""
        triggers_path = self.repo_root / "doc_agent" / "orchestration" / "agent-triggers.yaml"
        if not triggers_path.exists():
            return None
        
        try:
            with open(triggers_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                return set(config.get("triggers", {}).keys())
        except Exception as e:
            print(f"[warn] agent-triggers.yaml: {e}", file=sys.stderr)
            return None
    
    def _extract_yaml_front_matter(self, md_text: str) -> Optional[Dict[str, Any]]:
        """MarkdownYAML Front Matter"""
        match = YAML_FRONT_MATTER_RE.match(md_text)
        if not match:
            return None
        
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            raise ValueError(f"YAML: {e}")
    
    def _validate_basic_fields(self, yaml_data: Dict[str, Any], file_path: str) -> None:
        """"""
        for field in self.required_fields:
            if field not in yaml_data or not yaml_data[field]:
                self.add_issue(LintIssue(
                    file=file_path,
                    severity=Severity.ERROR,
                    message=f": {field}",
                    fix=f"YAML Front Matter {field} "
                ))
        
        # spec_version
        if "spec_version" in yaml_data:
            if not re.match(r"^\d+\.\d+$", str(yaml_data["spec_version"])):
                self.add_issue(LintIssue(
                    file=file_path,
                    severity=Severity.ERROR,
                    message=f"spec_version: {yaml_data['spec_version']}",
                    fix="spec_version'X.Y''1.0'"
                ))
        
        # agent_id
        if "agent_id" in yaml_data:
            agent_id = yaml_data["agent_id"]
            if agent_id != "repo" and not agent_id.startswith("modules."):
                self.add_issue(LintIssue(
                    file=file_path,
                    severity=Severity.WARNING,
                    message=f"agent_id: {agent_id}",
                    fix=": 'repo''modules.<entity>.<instance>'"
                ))
    
    def _validate_with_schema(self, yaml_data: Dict[str, Any], file_path: str) -> None:
        """jsonschema"""
        if not self.has_jsonschema or not self.schema:
            return
        
        import jsonschema
        try:
            jsonschema.validate(instance=yaml_data, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            self.add_issue(LintIssue(
                file=file_path,
                severity=Severity.ERROR,
                message=f"Schema: {e.message}",
                rule="schema",
                fix=f": {'.'.join(str(p) for p in e.path)}"
            ))
        except Exception as e:
            self.add_issue(LintIssue(
                file=file_path,
                severity=Severity.WARNING,
                message=f"Schema: {e}",
                rule="schema"
            ))
    
    def _check_context_routes(self, yaml_data: Dict[str, Any], file_path: str) -> None:
        """context_routes"""
        if "context_routes" not in yaml_data:
            return
        
        routes = yaml_data["context_routes"]
        if not isinstance(routes, dict):
            return
        
        # always_read
        if "always_read" in routes:
            for path in routes["always_read"]:
                if not path.startswith("/"):
                    self.add_issue(LintIssue(
                        file=file_path,
                        severity=Severity.WARNING,
                        message=f"/: {path}",
                        fix="/"
                    ))
                else:
                    full_path = self.repo_root / path.lstrip("/")
                    if not full_path.exists():
                        self.add_issue(LintIssue(
                            file=file_path,
                            severity=Severity.WARNING,
                            message=f"always_read: {path}",
                            fix=f": {full_path}"
                        ))
        
        # on_demand
        if "on_demand" in routes:
            for item in routes["on_demand"]:
                if "paths" in item:
                    topic = item.get('topic', 'unknown')
                    for path in item["paths"]:
                        if not path.startswith("/"):
                            self.add_issue(LintIssue(
                                file=file_path,
                                severity=Severity.WARNING,
                                message=f"[{topic}] /: {path}"
                            ))
                        else:
                            full_path = self.repo_root / path.lstrip("/")
                            if not full_path.exists():
                                self.add_issue(LintIssue(
                                    file=file_path,
                                    severity=Severity.WARNING,
                                    message=f"[{topic}] : {path}"
                                ))
        
        # by_scope
        if "by_scope" in routes:
            for item in routes["by_scope"]:
                scope = item.get('scope', 'unknown')
                if "read" in item:
                    for path in item["read"]:
                        if not path.startswith("/"):
                            self.add_issue(LintIssue(
                                file=file_path,
                                severity=Severity.WARNING,
                                message=f"[{scope}] /: {path}"
                            ))
                        else:
                            full_path = self.repo_root / path.lstrip("/")
                            if not full_path.exists():
                                self.add_issue(LintIssue(
                                    file=file_path,
                                    severity=Severity.WARNING,
                                    message=f"[{scope}] : {path}"
                                ))
    
    def _check_trigger_config(self, yaml_data: Dict[str, Any], file_path: str) -> None:
        """trigger_config"""
        if "trigger_config" not in yaml_data:
            return  # 
        
        if not self.trigger_rules:
            return  # 
        
        trigger_config = yaml_data["trigger_config"]
        
        # rules
        if "rules" in trigger_config:
            for rule_id in trigger_config["rules"]:
                if rule_id not in self.trigger_rules:
                    self.add_issue(LintIssue(
                        file=file_path,
                        severity=Severity.WARNING,
                        message=f": {rule_id}",
                        fix="doc_agent/orchestration/agent-triggers.yamlID"
                    ))
        
        # exclude_rules
        if "exclude_rules" in trigger_config:
            for rule_id in trigger_config["exclude_rules"]:
                if rule_id not in self.trigger_rules:
                    self.add_issue(LintIssue(
                        file=file_path,
                        severity=Severity.WARNING,
                        message=f"exclude_rules: {rule_id}"
                    ))
        
        # custom_triggers
        if "custom_triggers" in trigger_config:
            for custom in trigger_config["custom_triggers"]:
                if "load_documents" in custom:
                    for doc in custom["load_documents"]:
                        if "path" in doc:
                            path = doc["path"]
                            full_path = self.repo_root / path.lstrip("/")
                            if not full_path.exists():
                                self.add_issue(LintIssue(
                                    file=file_path,
                                    severity=Severity.WARNING,
                                    message=f"custom_triggers: {path}"
                                ))
    
    def _check_agent_file(self, agent_path: Path) -> None:
        """agent.md"""
        rel_path = str(agent_path.relative_to(self.repo_root))
        
        try:
            with open(agent_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # YAML Front Matter
            yaml_data = self._extract_yaml_front_matter(content)
            if not yaml_data:
                self.add_issue(LintIssue(
                    file=rel_path,
                    severity=Severity.ERROR,
                    message="YAML Front Matter",
                    fix="agent.md --- YAML"
                ))
                return
            
            # 
            self._validate_basic_fields(yaml_data, rel_path)
            
            # Schema
            self._validate_with_schema(yaml_data, rel_path)
            
            # context_routes
            self._check_context_routes(yaml_data, rel_path)
            
            # trigger_config
            self._check_trigger_config(yaml_data, rel_path)
            
        except ValueError as e:
            # YAML
            self.add_issue(LintIssue(
                file=rel_path,
                severity=Severity.ERROR,
                message=str(e)
            ))
        except Exception as e:
            self.add_issue(LintIssue(
                file=rel_path,
                severity=Severity.ERROR,
                message=f": {e}"
            ))
    
    def _find_agent_files(self) -> List[Path]:
        """agent.md"""
        agent_files = []
        
        # agent.md
        root_agent = self.repo_root / "agent.md"
        if root_agent.exists():
            agent_files.append(root_agent)
        
        # modules/*/agent.md
        modules_dir = self.repo_root / "modules"
        if modules_dir.exists():
            for agent_path in modules_dir.rglob("agent.md"):
                agent_files.append(agent_path)
        
        # agent.mdai/, config/, tools/
        for pattern in ["*/agent.md", "*/*/agent.md"]:
            for agent_path in self.repo_root.glob(pattern):
                # 
                if agent_path not in agent_files:
                    # node_modules, .git, temp
                    if not any(part.startswith(".") or part in ["node_modules", "temp", "tmp"] 
                              for part in agent_path.parts):
                        agent_files.append(agent_path)
        
        return agent_files
    
    def check(self) -> bool:
        """"""
        # jsonschema
        if self.has_jsonschema:
            print("\n✅ jsonschemaSchema")
        else:
            print("\n⚠️  jsonschema")
            print("   pip install jsonschema ")
        
        # agent.md
        agent_files = self._find_agent_files()
        
        if not agent_files:
            print("\nagent.md")
            return True
        
        print(f"\n {len(agent_files)} agent.md")
        for agent_path in agent_files:
            rel_path = agent_path.relative_to(self.repo_root)
            print(f"  - {rel_path}")
        
        # 
        self.print_separator()
        print("")
        self.print_separator()
        
        for agent_path in agent_files:
            self.stats['files_checked'] += 1
            self._check_agent_file(agent_path)
        
        return self.stats['errors'] == 0


def main():
    """"""
    return run_linter(AgentLinter)


if __name__ == "__main__":
    sys.exit(main())