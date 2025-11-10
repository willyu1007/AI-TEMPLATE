#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent_lint.py - agent.md YAML前言校验工具（使用统一基础Lint框架）

功能：
1. 遍历仓库内所有agent.md文件
2. 提取YAML Front Matter
3. 进行基础必填字段校验
4. 使用schemas/agent.schema.yaml进行Schema校验（如jsonschema已安装）
5. 校验context_routes中引用的路径
6. 校验trigger_config配置

用法：
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

# 导入基础Lint类
from base_lint import BaseLinter, LintIssue, Severity, run_linter

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "agent.schema.yaml"

# YAML Front Matter正则
YAML_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


class AgentLinter(BaseLinter):
    """agent.md文件校验器"""
    
    @property
    def name(self) -> str:
        """Linter名称"""
        return "Agent"
    
    def __init__(self, repo_root: Optional[Path] = None):
        """初始化"""
        super().__init__(repo_root)
        self.schema = self._load_schema()
        self.has_jsonschema = self._check_jsonschema()
        self.required_fields = ["spec_version", "agent_id", "role"]
        self.trigger_rules = self._load_trigger_rules()
    
    def _load_schema(self) -> Optional[Dict[str, Any]]:
        """加载agent.schema.yaml"""
        if not SCHEMA_PATH.exists():
            return None
        try:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[warn] 无法加载Schema: {e}", file=sys.stderr)
            return None
    
    def _check_jsonschema(self) -> bool:
        """检查jsonschema是否可用"""
        try:
            import jsonschema
            return True
        except ImportError:
            return False
    
    def _load_trigger_rules(self) -> Optional[set]:
        """加载agent-triggers.yaml中的触发规则ID列表"""
        triggers_path = self.repo_root / "doc_agent" / "orchestration" / "agent-triggers.yaml"
        if not triggers_path.exists():
            return None
        
        try:
            with open(triggers_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                return set(config.get("triggers", {}).keys())
        except Exception as e:
            print(f"[warn] 无法加载agent-triggers.yaml: {e}", file=sys.stderr)
            return None
    
    def _extract_yaml_front_matter(self, md_text: str) -> Optional[Dict[str, Any]]:
        """从Markdown文件中提取YAML Front Matter"""
        match = YAML_FRONT_MATTER_RE.match(md_text)
        if not match:
            return None
        
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            raise ValueError(f"YAML解析错误: {e}")
    
    def _validate_basic_fields(self, yaml_data: Dict[str, Any], file_path: str) -> None:
        """基础字段校验（必填检查）"""
        for field in self.required_fields:
            if field not in yaml_data or not yaml_data[field]:
                self.add_issue(LintIssue(
                    file=file_path,
                    severity=Severity.ERROR,
                    message=f"缺失必填字段: {field}",
                    fix=f"在YAML Front Matter中添加 {field} 字段"
                ))
        
        # spec_version格式检查
        if "spec_version" in yaml_data:
            if not re.match(r"^\d+\.\d+$", str(yaml_data["spec_version"])):
                self.add_issue(LintIssue(
                    file=file_path,
                    severity=Severity.ERROR,
                    message=f"spec_version格式错误: {yaml_data['spec_version']}",
                    fix="spec_version应为'X.Y'格式，如'1.0'"
                ))
        
        # agent_id格式检查
        if "agent_id" in yaml_data:
            agent_id = yaml_data["agent_id"]
            if agent_id != "repo" and not agent_id.startswith("modules."):
                self.add_issue(LintIssue(
                    file=file_path,
                    severity=Severity.WARNING,
                    message=f"agent_id格式不规范: {agent_id}",
                    fix="建议格式: 'repo'或'modules.<entity>.<instance>'"
                ))
    
    def _validate_with_schema(self, yaml_data: Dict[str, Any], file_path: str) -> None:
        """使用jsonschema验证数据"""
        if not self.has_jsonschema or not self.schema:
            return
        
        import jsonschema
        try:
            jsonschema.validate(instance=yaml_data, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            self.add_issue(LintIssue(
                file=file_path,
                severity=Severity.ERROR,
                message=f"Schema校验失败: {e.message}",
                rule="schema",
                fix=f"检查字段: {'.'.join(str(p) for p in e.path)}"
            ))
        except Exception as e:
            self.add_issue(LintIssue(
                file=file_path,
                severity=Severity.WARNING,
                message=f"Schema校验异常: {e}",
                rule="schema"
            ))
    
    def _check_context_routes(self, yaml_data: Dict[str, Any], file_path: str) -> None:
        """检查context_routes的路径是否存在"""
        if "context_routes" not in yaml_data:
            return
        
        routes = yaml_data["context_routes"]
        if not isinstance(routes, dict):
            return
        
        # 检查always_read路径
        if "always_read" in routes:
            for path in routes["always_read"]:
                if not path.startswith("/"):
                    self.add_issue(LintIssue(
                        file=file_path,
                        severity=Severity.WARNING,
                        message=f"路径应以/开头: {path}",
                        fix="路径应相对于仓库根目录，以/开头"
                    ))
                else:
                    full_path = self.repo_root / path.lstrip("/")
                    if not full_path.exists():
                        self.add_issue(LintIssue(
                            file=file_path,
                            severity=Severity.WARNING,
                            message=f"always_read路径不存在: {path}",
                            fix=f"确保文件存在: {full_path}"
                        ))
        
        # 检查on_demand路径
        if "on_demand" in routes:
            for item in routes["on_demand"]:
                if "paths" in item:
                    topic = item.get('topic', 'unknown')
                    for path in item["paths"]:
                        if not path.startswith("/"):
                            self.add_issue(LintIssue(
                                file=file_path,
                                severity=Severity.WARNING,
                                message=f"[{topic}] 路径应以/开头: {path}"
                            ))
                        else:
                            full_path = self.repo_root / path.lstrip("/")
                            if not full_path.exists():
                                self.add_issue(LintIssue(
                                    file=file_path,
                                    severity=Severity.WARNING,
                                    message=f"[{topic}] 路径不存在: {path}"
                                ))
        
        # 检查by_scope路径
        if "by_scope" in routes:
            for item in routes["by_scope"]:
                scope = item.get('scope', 'unknown')
                if "read" in item:
                    for path in item["read"]:
                        if not path.startswith("/"):
                            self.add_issue(LintIssue(
                                file=file_path,
                                severity=Severity.WARNING,
                                message=f"[{scope}] 路径应以/开头: {path}"
                            ))
                        else:
                            full_path = self.repo_root / path.lstrip("/")
                            if not full_path.exists():
                                self.add_issue(LintIssue(
                                    file=file_path,
                                    severity=Severity.WARNING,
                                    message=f"[{scope}] 路径不存在: {path}"
                                ))
    
    def _check_trigger_config(self, yaml_data: Dict[str, Any], file_path: str) -> None:
        """校验trigger_config字段"""
        if "trigger_config" not in yaml_data:
            return  # 可选字段
        
        if not self.trigger_rules:
            return  # 无法加载触发规则
        
        trigger_config = yaml_data["trigger_config"]
        
        # 检查rules字段
        if "rules" in trigger_config:
            for rule_id in trigger_config["rules"]:
                if rule_id not in self.trigger_rules:
                    self.add_issue(LintIssue(
                        file=file_path,
                        severity=Severity.WARNING,
                        message=f"引用了不存在的触发规则: {rule_id}",
                        fix="检查doc_agent/orchestration/agent-triggers.yaml中的规则ID"
                    ))
        
        # 检查exclude_rules字段
        if "exclude_rules" in trigger_config:
            for rule_id in trigger_config["exclude_rules"]:
                if rule_id not in self.trigger_rules:
                    self.add_issue(LintIssue(
                        file=file_path,
                        severity=Severity.WARNING,
                        message=f"exclude_rules引用了不存在的规则: {rule_id}"
                    ))
        
        # 检查custom_triggers中的文档路径
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
                                    message=f"custom_triggers文档路径不存在: {path}"
                                ))
    
    def _check_agent_file(self, agent_path: Path) -> None:
        """校验单个agent.md文件"""
        rel_path = str(agent_path.relative_to(self.repo_root))
        
        try:
            with open(agent_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 提取YAML Front Matter
            yaml_data = self._extract_yaml_front_matter(content)
            if not yaml_data:
                self.add_issue(LintIssue(
                    file=rel_path,
                    severity=Severity.ERROR,
                    message="未找到YAML Front Matter",
                    fix="agent.md文件应以 --- 开头并包含YAML前言"
                ))
                return
            
            # 基础字段校验
            self._validate_basic_fields(yaml_data, rel_path)
            
            # Schema校验（如果可用）
            self._validate_with_schema(yaml_data, rel_path)
            
            # context_routes路径校验
            self._check_context_routes(yaml_data, rel_path)
            
            # trigger_config校验
            self._check_trigger_config(yaml_data, rel_path)
            
        except ValueError as e:
            # YAML解析错误
            self.add_issue(LintIssue(
                file=rel_path,
                severity=Severity.ERROR,
                message=str(e)
            ))
        except Exception as e:
            self.add_issue(LintIssue(
                file=rel_path,
                severity=Severity.ERROR,
                message=f"读取文件失败: {e}"
            ))
    
    def _find_agent_files(self) -> List[Path]:
        """查找所有agent.md文件"""
        agent_files = []
        
        # 根目录的agent.md
        root_agent = self.repo_root / "agent.md"
        if root_agent.exists():
            agent_files.append(root_agent)
        
        # modules/*/agent.md
        modules_dir = self.repo_root / "modules"
        if modules_dir.exists():
            for agent_path in modules_dir.rglob("agent.md"):
                agent_files.append(agent_path)
        
        # 其他目录的agent.md（如ai/, config/, tools/等）
        for pattern in ["*/agent.md", "*/*/agent.md"]:
            for agent_path in self.repo_root.glob(pattern):
                # 避免重复
                if agent_path not in agent_files:
                    # 排除node_modules, .git, temp等
                    if not any(part.startswith(".") or part in ["node_modules", "temp", "tmp"] 
                              for part in agent_path.parts):
                        agent_files.append(agent_path)
        
        return agent_files
    
    def check(self) -> bool:
        """执行检查"""
        # 检查jsonschema是否可用
        if self.has_jsonschema:
            print("\n✅ jsonschema已安装，将进行Schema校验")
        else:
            print("\n⚠️  jsonschema未安装，仅进行基础校验")
            print("   提示：pip install jsonschema 可启用完整校验")
        
        # 查找所有agent.md文件
        agent_files = self._find_agent_files()
        
        if not agent_files:
            print("\n未找到任何agent.md文件")
            return True
        
        print(f"\n找到 {len(agent_files)} 个agent.md文件：")
        for agent_path in agent_files:
            rel_path = agent_path.relative_to(self.repo_root)
            print(f"  - {rel_path}")
        
        # 校验每个文件
        self.print_separator()
        print("开始校验")
        self.print_separator()
        
        for agent_path in agent_files:
            self.stats['files_checked'] += 1
            self._check_agent_file(agent_path)
        
        return self.stats['errors'] == 0


def main():
    """主函数"""
    return run_linter(AgentLinter)


if __name__ == "__main__":
    sys.exit(main())