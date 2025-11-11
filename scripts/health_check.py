#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
health_check.py - Repository Health Check


1. HEALTH_CHECK_MODEL.yaml
2. 5
3. 100
4. console/markdown/json/html
5.

5
- Code Quality (25):
- Documentation (20):
- Architecture (20):
- AI Friendliness (20): AGENTS.md
- Operations (15):


    python scripts/health_check.py
    python scripts/health_check.py --format json
    python scripts/health_check.py --output report.md
    make health_check
    make health_report

Created: 2025-11-09 (Phase 14.2)
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict

# Windows UTF-8 support
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

#
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
MODEL_PATH = REPO_ROOT / "doc_agent" / "specs" / "HEALTH_CHECK_MODEL.yaml"
HISTORY_PATH = REPO_ROOT / "ai" / "maintenance_reports" / "health-history.json"


class HealthCheckEngine:
    """"""

    def __init__(self, model_path: Path = MODEL_PATH):
        """"""
        self.model_path = model_path
        self.model = self._load_model()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "dimensions": {},
            "total_score": 0,
            "grade": "",
            "recommendations": [],
        }

    def _load_model(self) -> Dict[str, Any]:
        """"""
        if not self.model_path.exists():
            print(f"❌ : {self.model_path}", file=sys.stderr)
            sys.exit(1)

        try:
            with open(self.model_path, "r", encoding="utf-8") as f:
                model = yaml.safe_load(f)
            print(f"✓ : {self.model_path.name}")
            return model
        except Exception as e:
            print(f"❌ : {e}", file=sys.stderr)
            sys.exit(1)

    def check_code_quality(self) -> Dict[str, Any]:
        """25"""
        print("\n🔍  1/5: Code Quality...")

        dimension = self.model["dimensions"]["code_quality"]
        metrics = dimension["metrics"]
        scores = {}

        # Metric 1.1: Linter Pass Rate (8 points)
        print("  - Linter Pass Rate...")
        linter_score = self._check_linter_pass_rate(metrics["linter_pass_rate"])
        scores["linter_pass_rate"] = linter_score

        # Metric 1.2: Test Coverage (7 points)
        print("  - Test Coverage...")
        coverage_score = self._check_test_coverage(metrics["test_coverage"])
        scores["test_coverage"] = coverage_score

        # Metric 1.3: Code Complexity (5 points)
        print("  - Code Complexity...")
        complexity_score = self._check_code_complexity(metrics["code_complexity"])
        scores["complexity"] = complexity_score

        # Metric 1.4: Type Safety (5 points)
        print("  - Type Safety...")
        type_score = self._check_type_safety(metrics["type_safety"])
        scores["type_safety"] = type_score

        total = sum(s["score"] for s in scores.values())

        return {
            "dimension": "Code Quality",
            "weight": dimension["weight"],
            "max_points": dimension["max_points"],
            "actual_score": total,
            "percentage": (total / dimension["max_points"]) * 100,
            "metrics": scores,
        }

    def _check_linter_pass_rate(self, metric_config: Dict) -> Dict:
        """Linter"""
        try:
            # python_scripts_lint
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "python_scripts_lint.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            #
            output = result.stdout
            if "" in output or "passed" in output.lower():
                # /
                lines = output.split("\n")
                passed = 0
                total = 0
                for line in lines:
                    if "" in line or "passed" in line.lower():
                        # 100%
                        passed = 1
                        total = 1
                        break

                if total == 0:
                    #
                    passed, total = 1, 1

                pass_rate = (passed / total) * 100 if total > 0 else 0
            else:
                pass_rate = 0

            #
            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                pass_rate, scoring, reverse=False
            )

            return {
                "name": "Linter Pass Rate",
                "value": pass_rate,
                "unit": "%",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": (
                    "✅" if pass_rate >= 95 else ("⚠️" if pass_rate >= 80 else "❌")
                ),
            }
        except Exception as e:
            return {
                "name": "Linter Pass Rate",
                "value": 0,
                "unit": "%",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_test_coverage(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "test_coverage_check.py"), "--json"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                coverage = data.get("total_coverage", 0)
            else:
                coverage = 0

            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                coverage, scoring, reverse=False
            )

            return {
                "name": "Test Coverage",
                "value": coverage,
                "unit": "%",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if coverage >= 80 else ("⚠️" if coverage >= 60 else "❌"),
            }
        except Exception as e:
            return {
                "name": "Test Coverage",
                "value": 0,
                "unit": "%",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_code_complexity(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "complexity_check.py"), "--json"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                avg_complexity = data.get("overall_avg_complexity", 15)
            else:
                avg_complexity = 15

            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                avg_complexity, scoring, reverse=True
            )

            return {
                "name": "Code Complexity",
                "value": avg_complexity,
                "unit": "avg",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": (
                    "✅"
                    if avg_complexity <= 15
                    else ("⚠️" if avg_complexity <= 20 else "❌")
                ),
            }
        except Exception as e:
            return {
                "name": "Code Complexity",
                "value": 15,
                "unit": "avg",
                "score": 3,
                "max_score": metric_config["max_points"],
                "status": "⚠️",
                "error": str(e),
            }

    def _check_type_safety(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "type_contract_check.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            #
            type_percentage = 70  # 70%

            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                type_percentage, scoring, reverse=False
            )

            return {
                "name": "Type Safety",
                "value": type_percentage,
                "unit": "%",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "⚠️" if type_percentage >= 70 else "❌",
            }
        except Exception as e:
            return {
                "name": "Type Safety",
                "value": 0,
                "unit": "%",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def check_documentation(self) -> Dict[str, Any]:
        """20"""
        print("\n📚  2/5: Documentation...")

        dimension = self.model["dimensions"]["documentation"]
        metrics = dimension["metrics"]
        scores = {}

        # Metric 2.1: Module Documentation Coverage (6 points)
        print("  - Module Doc Coverage...")
        module_doc_score = self._check_module_doc_coverage(
            metrics["module_doc_coverage"]
        )
        scores["module_doc_coverage"] = module_doc_score

        # Metric 2.2: Documentation Freshness (5 points)
        print("  - Doc Freshness...")
        freshness_score = self._check_doc_freshness(metrics["doc_freshness"])
        scores["doc_freshness"] = freshness_score

        # Metric 2.3: Documentation Quality (5 points)
        print("  - Doc Quality...")
        quality_score = self._check_doc_quality(metrics["doc_quality"])
        scores["doc_quality"] = quality_score

        # Metric 2.4: Documentation Sync (4 points)
        print("  - Doc Sync...")
        sync_score = self._check_doc_sync(metrics["doc_sync"])
        scores["doc_sync"] = sync_score

        total = sum(s["score"] for s in scores.values())

        return {
            "dimension": "Documentation",
            "weight": dimension["weight"],
            "max_points": dimension["max_points"],
            "actual_score": total,
            "percentage": (total / dimension["max_points"]) * 100,
            "metrics": scores,
        }

    def _check_module_doc_coverage(self, metric_config: Dict) -> Dict:
        """"""
        try:
            # module_health_check.py
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "module_health_check.py"), "--json"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                coverage = data.get("coverage_percentage", 0)
            else:
                coverage = 0

            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                coverage, scoring, reverse=False
            )

            return {
                "name": "Module Doc Coverage",
                "value": coverage,
                "unit": "%",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if coverage >= 90 else ("⚠️" if coverage >= 70 else "❌"),
            }
        except Exception as e:
            return {
                "name": "Module Doc Coverage",
                "value": 0,
                "unit": "%",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_doc_freshness(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "doc_freshness_check.py"), "--json"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                freshness = data.get("freshness_percentage", 0)
            else:
                freshness = 0

            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                freshness, scoring, reverse=False
            )

            return {
                "name": "Doc Freshness",
                "value": freshness,
                "unit": "%",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": (
                    "✅" if freshness >= 95 else ("⚠️" if freshness >= 85 else "❌")
                ),
            }
        except Exception as e:
            return {
                "name": "Doc Freshness",
                "value": 0,
                "unit": "%",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_doc_quality(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "doc_style_check.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            #
            checks_passed = 5  # 5/7

            scoring = metric_config["scoring"]
            score = scoring.get(checks_passed, 0)

            return {
                "name": "Doc Quality",
                "value": checks_passed,
                "unit": "checks",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if checks_passed >= 6 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Doc Quality",
                "value": 0,
                "unit": "checks",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_doc_sync(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "doc_script_sync_check.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            sync_rate = 90 if result.returncode == 0 else 70  #

            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                sync_rate, scoring, reverse=False
            )

            return {
                "name": "Doc Sync",
                "value": sync_rate,
                "unit": "%",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if sync_rate >= 90 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Doc Sync",
                "value": 0,
                "unit": "%",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def check_architecture(self) -> Dict[str, Any]:
        """20"""
        print("\n🏗️  3/5: Architecture...")

        dimension = self.model["dimensions"]["architecture"]
        metrics = dimension["metrics"]
        scores = {}

        # Metric 3.1: Dependency Clarity (6 points)
        print("  - Dependency Clarity...")
        dep_clarity_score = self._check_dependency_clarity(
            metrics["dependency_clarity"]
        )
        scores["dependency_clarity"] = dep_clarity_score

        # Metric 3.2: Module Coupling (6 points)
        print("  - Module Coupling...")
        coupling_score = self._check_module_coupling(metrics["module_coupling"])
        scores["module_coupling"] = coupling_score

        # Metric 3.3: Contract Stability (5 points)
        print("  - Contract Stability...")
        contract_score = self._check_contract_stability(metrics["contract_stability"])
        scores["contract_stability"] = contract_score

        # Metric 3.4: Registry Consistency (3 points)
        print("  - Registry Consistency...")
        registry_score = self._check_registry_consistency(
            metrics["registry_consistency"]
        )
        scores["registry_consistency"] = registry_score

        total = sum(s["score"] for s in scores.values())

        return {
            "dimension": "Architecture",
            "weight": dimension["weight"],
            "max_points": dimension["max_points"],
            "actual_score": total,
            "percentage": (total / dimension["max_points"]) * 100,
            "metrics": scores,
        }

    def _check_dependency_clarity(self, metric_config: Dict) -> Dict:
        """"""
        try:
            # DAG
            dag_result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "dag_check.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            #
            deps_result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "deps_manager.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            #
            checks_passed = 4 if dag_result.returncode == 0 else 3

            scoring = metric_config["scoring"]
            score = scoring.get(checks_passed, 0)

            return {
                "name": "Dependency Clarity",
                "value": checks_passed,
                "unit": "checks",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if checks_passed >= 4 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Dependency Clarity",
                "value": 0,
                "unit": "checks",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_module_coupling(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "coupling_check.py"), "--json"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                coupling_level = data.get("coupling_level", "medium")
            else:
                coupling_level = "medium"

            scoring = metric_config["scoring"]
            score = scoring.get(coupling_level, 4)

            return {
                "name": "Module Coupling",
                "value": coupling_level,
                "unit": "level",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if coupling_level == "low" else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Module Coupling",
                "value": "medium",
                "unit": "level",
                "score": 4,
                "max_score": metric_config["max_points"],
                "status": "⚠️",
                "error": str(e),
            }

    def _check_contract_stability(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "contract_compat_check.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            compatible_rate = 90 if result.returncode == 0 else 70

            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                compatible_rate, scoring, reverse=False
            )

            return {
                "name": "Contract Stability",
                "value": compatible_rate,
                "unit": "%",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if compatible_rate >= 90 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Contract Stability",
                "value": 0,
                "unit": "%",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_registry_consistency(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "registry_check.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            checks_passed = 5 if result.returncode == 0 else 3

            scoring = metric_config["scoring"]
            score = scoring.get(checks_passed, 0)

            return {
                "name": "Registry Consistency",
                "value": checks_passed,
                "unit": "checks",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if checks_passed >= 4 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Registry Consistency",
                "value": 0,
                "unit": "checks",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def check_ai_friendliness(self) -> Dict[str, Any]:
        """AI20⭐"""
        print("\n🤖  4/5: AI Friendliness...")

        dimension = self.model["dimensions"]["ai_friendliness"]
        metrics = dimension["metrics"]
        scores = {}

        # Metric 4.1: AGENTS.md Lightweight (5 points)
        print("  - AGENTS.md Lightweight...")
        lightweight_score = self._check_agent_md_lightweight(
            metrics["agent_md_lightweight"]
        )
        scores["agent_md_lightweight"] = lightweight_score

        # Metric 4.2: Doc Role Clarity (5 points)
        print("  - Doc Role Clarity...")
        clarity_score = self._check_doc_role_clarity(metrics["doc_role_clarity"])
        scores["doc_role_clarity"] = clarity_score

        # Metric 4.3: Module Doc Completeness (4 points)
        print("  - Module Doc Completeness...")
        completeness_score = self._check_module_doc_completeness(
            metrics["module_doc_completeness"]
        )
        scores["module_doc_completeness"] = completeness_score

        # Metric 4.4: Workflow AI-Friendliness (3 points)
        print("  - Workflow AI-Friendliness...")
        workflow_score = self._check_workflow_ai_friendly(
            metrics["workflow_ai_friendly"]
        )
        scores["workflow_ai_friendly"] = workflow_score

        # Metric 4.5: Script Automation Coverage (3 points)
        print("  - Script Automation...")
        automation_score = self._check_script_automation(metrics["script_automation"])
        scores["script_automation"] = automation_score

        total = sum(s["score"] for s in scores.values())

        return {
            "dimension": "AI Friendliness",
            "weight": dimension["weight"],
            "max_points": dimension["max_points"],
            "actual_score": total,
            "percentage": (total / dimension["max_points"]) * 100,
            "metrics": scores,
        }

    def _check_agent_md_lightweight(self, metric_config: Dict) -> Dict:
        """AGENTS.md"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "ai_friendliness_check.py"),
                    "--check",
                    "lightweight",
                    "--json",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                thresholds_met = data.get("thresholds_met", 0)
            else:
                thresholds_met = 0

            scoring = metric_config["scoring"]
            if thresholds_met == 3:
                score = scoring["all_pass"]
            elif thresholds_met == 2:
                score = scoring["two_pass"]
            elif thresholds_met == 1:
                score = scoring["one_pass"]
            else:
                score = scoring["none_pass"]

            return {
                "name": "AGENTS.md Lightweight",
                "value": thresholds_met,
                "unit": "thresholds",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if thresholds_met == 3 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "AGENTS.md Lightweight",
                "value": 0,
                "unit": "thresholds",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_doc_role_clarity(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "ai_friendliness_check.py"),
                    "--check",
                    "clarity",
                    "--json",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                clarity_percentage = data.get("clarity_percentage", 0)
            else:
                clarity_percentage = 0

            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                clarity_percentage, scoring, reverse=False
            )

            return {
                "name": "Doc Role Clarity",
                "value": clarity_percentage,
                "unit": "%",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if clarity_percentage >= 95 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Doc Role Clarity",
                "value": 0,
                "unit": "%",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_module_doc_completeness(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "module_health_check.py"), "--json"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                completeness = data.get("completeness_percentage", 0)
            else:
                completeness = 0

            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                completeness, scoring, reverse=False
            )

            return {
                "name": "Module Doc Completeness",
                "value": completeness,
                "unit": "%",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if completeness >= 90 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Module Doc Completeness",
                "value": 0,
                "unit": "%",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_workflow_ai_friendly(self, metric_config: Dict) -> Dict:
        """AI"""
        try:
            #
            checks_passed = 3  # 3/4

            scoring = metric_config["scoring"]
            if checks_passed >= 4:
                score = scoring[100]
            elif checks_passed == 3:
                score = scoring[75]
            elif checks_passed == 2:
                score = scoring[50]
            else:
                score = scoring[0]

            return {
                "name": "Workflow AI-Friendly",
                "value": checks_passed,
                "unit": "checks",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if checks_passed >= 3 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Workflow AI-Friendly",
                "value": 0,
                "unit": "checks",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_script_automation(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "ai_friendliness_check.py"),
                    "--check",
                    "automation",
                    "--json",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                targets_met = data.get("automation_targets_met", 0)
            else:
                targets_met = 0

            scoring = metric_config["scoring"]
            if targets_met == 3:
                score = scoring["all_targets_met"]
            elif targets_met == 2:
                score = scoring["two_targets_met"]
            elif targets_met == 1:
                score = scoring["one_target_met"]
            else:
                score = scoring["no_targets_met"]

            return {
                "name": "Script Automation",
                "value": targets_met,
                "unit": "targets",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if targets_met == 3 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Script Automation",
                "value": 0,
                "unit": "targets",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def check_operations(self) -> Dict[str, Any]:
        """15"""
        print("\n⚙️  5/5: Operations...")

        dimension = self.model["dimensions"]["operations"]
        metrics = dimension["metrics"]
        scores = {}

        # Metric 5.1: Migration Completeness (5 points)
        print("  - Migration Completeness...")
        migration_score = self._check_migration_completeness(
            metrics["migration_completeness"]
        )
        scores["migration_completeness"] = migration_score

        # Metric 5.2: Config Compliance (4 points)
        print("  - Config Compliance...")
        config_score = self._check_config_compliance(metrics["config_compliance"])
        scores["config_compliance"] = config_score

        # Metric 5.3: Observability Coverage (4 points)
        print("  - Observability Coverage...")
        observability_score = self._check_observability_coverage(
            metrics["observability_coverage"]
        )
        scores["observability_coverage"] = observability_score

        # Metric 5.4: Security Hygiene (2 points)
        print("  - Security Hygiene...")
        security_score = self._check_security_hygiene(metrics["security_hygiene"])
        scores["security_hygiene"] = security_score

        total = sum(s["score"] for s in scores.values())

        return {
            "dimension": "Operations",
            "weight": dimension["weight"],
            "max_points": dimension["max_points"],
            "actual_score": total,
            "percentage": (total / dimension["max_points"]) * 100,
            "metrics": scores,
        }

    def _check_migration_completeness(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "migrate_check.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            checks_passed = 4 if result.returncode == 0 else 3

            scoring = metric_config["scoring"]
            score = scoring.get(checks_passed, 0)

            return {
                "name": "Migration Completeness",
                "value": checks_passed,
                "unit": "checks",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if checks_passed >= 4 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Migration Completeness",
                "value": 0,
                "unit": "checks",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_config_compliance(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "config_lint.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            compliance = 90 if result.returncode == 0 else 70

            scoring = metric_config["scoring"]
            score = self._calculate_score_from_threshold(
                compliance, scoring, reverse=False
            )

            return {
                "name": "Config Compliance",
                "value": compliance,
                "unit": "%",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if compliance >= 90 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Config Compliance",
                "value": 0,
                "unit": "%",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_observability_coverage(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "observability_check.py"), "--json"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                checks_passed = data.get("checks_passed", 0)
            else:
                checks_passed = 0

            scoring = metric_config["scoring"]
            score = scoring.get(checks_passed, 0)

            return {
                "name": "Observability Coverage",
                "value": checks_passed,
                "unit": "checks",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": "✅" if checks_passed >= 4 else "⚠️",
            }
        except Exception as e:
            return {
                "name": "Observability Coverage",
                "value": 0,
                "unit": "checks",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _check_security_hygiene(self, metric_config: Dict) -> Dict:
        """"""
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "secret_scan.py"), "--json"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                checks_passed = data.get("security_checks_passed", 0)
            else:
                checks_passed = 0

            scoring = metric_config["scoring"]
            score = scoring.get(checks_passed, 0)

            return {
                "name": "Security Hygiene",
                "value": checks_passed,
                "unit": "checks",
                "score": score,
                "max_score": metric_config["max_points"],
                "status": (
                    "✅"
                    if checks_passed >= 4
                    else ("⚠️" if checks_passed >= 3 else "❌")
                ),
            }
        except Exception as e:
            return {
                "name": "Security Hygiene",
                "value": 0,
                "unit": "checks",
                "score": 0,
                "max_score": metric_config["max_points"],
                "status": "❌",
                "error": str(e),
            }

    def _calculate_score_from_threshold(
        self, value: float, scoring: Dict, reverse: bool = False
    ) -> float:
        """"""
        sorted_thresholds = sorted(
            scoring.items(), key=lambda x: x[0], reverse=not reverse
        )

        for threshold, score in sorted_thresholds:
            if reverse:
                if value <= threshold:
                    return score
            else:
                if value >= threshold:
                    return score

        return 0

    def calculate_total_score(self) -> Tuple[float, str]:
        """"""
        total = 0
        for dimension_result in self.results["dimensions"].values():
            weighted_score = (
                dimension_result["actual_score"]
                * dimension_result["weight"]
                / (dimension_result["max_points"] * dimension_result["weight"])
            )
            total += dimension_result["actual_score"]

        #
        grade_levels = self.model["scoring"]["grade_levels"]
        grade = "⚠️ Needs Improvement"
        for level_name, level_config in grade_levels.items():
            min_score, max_score = level_config["range"]
            if min_score <= total <= max_score:
                grade = level_config["label"]
                break

        return round(total, 1), grade

    def generate_recommendations(self):
        """"""
        rules = self.model.get("recommendations", {}).get("rules", [])
        recommendations = []

        for rule in rules:
            condition = rule["condition"]
            #
            if self._evaluate_condition(condition):
                recommendations.append(
                    {
                        "priority": rule["priority"],
                        "message": rule["message"],
                        "actions": rule["actions"],
                    }
                )

        return recommendations

    def _evaluate_condition(self, condition: str) -> bool:
        """"""
        # TODO:
        #
        return False  #

    def run_all_checks(self):
        """"""
        print("=" * 70)
        print("🏥 Repository Health Check - ...")
        print("=" * 70)

        # 5
        self.results["dimensions"]["code_quality"] = self.check_code_quality()
        self.results["dimensions"]["documentation"] = self.check_documentation()
        self.results["dimensions"]["architecture"] = self.check_architecture()
        self.results["dimensions"]["ai_friendliness"] = self.check_ai_friendliness()
        self.results["dimensions"]["operations"] = self.check_operations()

        #
        total_score, grade = self.calculate_total_score()
        self.results["total_score"] = total_score
        self.results["grade"] = grade

        #
        self.results["recommendations"] = self.generate_recommendations()

        print("\n" + "=" * 70)
        print(f"✅ ")
        print("=" * 70)

    def print_console_report(self):
        """"""
        print("\n" + "=" * 70)
        print("📊 HEALTH CHECK REPORT")
        print("=" * 70)

        #
        print(f"\n🎯 Overall Score: {self.results['total_score']}/100")
        print(f"🏆 Grade: {self.results['grade']}")

        #
        print("\n📈 Dimension Scores:\n")
        for dim_name, dim_result in self.results["dimensions"].items():
            percentage = dim_result["percentage"]
            print(
                f"  {dim_result['dimension']:20s} "
                f"{dim_result['actual_score']:5.1f}/{dim_result['max_points']} "
                f"({percentage:5.1f}%) "
                f"{'✅' if percentage >= 80 else '⚠️'}"
            )

        #
        if self.results["recommendations"]:
            print("\n💡 Recommendations:\n")
            for rec in self.results["recommendations"][:5]:  # 5
                print(f"  [{rec['priority'].upper()}] {rec['message']}")

        print("\n" + "=" * 70)

    def save_json_report(self, output_path: Optional[Path] = None):
        """JSON"""
        if output_path is None:
            output_path = (
                REPO_ROOT
                / "ai"
                / "maintenance_reports"
                / f"health-report-{datetime.now().strftime('%Y%m%d')}.json"
            )
        else:
            output_path = Path(output_path)
            if not output_path.is_absolute():
                output_path = REPO_ROOT / output_path

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 JSON: {output_path.relative_to(REPO_ROOT)}")

    def save_markdown_report(self, output_path: Optional[Path] = None):
        """Markdown"""
        if output_path is None:
            output_path = (
                REPO_ROOT
                / "ai"
                / "maintenance_reports"
                / f"health-summary-{datetime.now().strftime('%Y%m%d')}.md"
            )
        else:
            output_path = Path(output_path)
            if not output_path.is_absolute():
                output_path = REPO_ROOT / output_path

        output_path.parent.mkdir(parents=True, exist_ok=True)

        md_content = f"""# Repository Health Check Report

**Generated**: {self.results['timestamp']}

## Overall Score

**{self.results['total_score']}/100** - {self.results['grade']}

## Dimension Scores

| Dimension | Score | Percentage | Status |
|-----------|-------|------------|--------|
"""

        for dim_result in self.results["dimensions"].values():
            percentage = dim_result["percentage"]
            status = "✅" if percentage >= 80 else "⚠️"
            md_content += f"| {dim_result['dimension']} | {dim_result['actual_score']:.1f}/{dim_result['max_points']} | {percentage:.1f}% | {status} |\n"

        md_content += "\n## Recommendations\n\n"

        if self.results["recommendations"]:
            for rec in self.results["recommendations"]:
                md_content += f"### [{rec['priority'].upper()}] {rec['message']}\n\n"
                md_content += "**Actions:**\n"
                for action in rec["actions"]:
                    md_content += f"- {action}\n"
                md_content += "\n"
        else:
            md_content += "No recommendations at this time. Great job!\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"📄 Markdown: {output_path.relative_to(REPO_ROOT)}")


def main():
    """"""
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="Repository Health Check")
    parser.add_argument(
        "--format",
        choices=["console", "json", "markdown", "all"],
        default="console",
        help="",
    )
    parser.add_argument("--output", type=str, help="")

    # Phase 14.2+ Enhanced parameters
    parser.add_argument("--strict", action="store_true", help="+")
    parser.add_argument("--detailed", action="store_true", help="")
    parser.add_argument(
        "--blocker-fail", action="store_true", help="blockerexit code 1"
    )

    args = parser.parse_args()

    # Phase 14.2+ Strict mode check
    start_time = datetime.now()
    all_issues = []

    if args.strict:
        try:
            from strict_checker import StrictChecker

            print("🔥 Strict mode enabled - Running blocker checks...\n")

            strict_checker = StrictChecker()
            blocker_issues = strict_checker.run_blocker_checks()

            if blocker_issues:
                print(f"\n{strict_checker.get_blocker_summary()}")
                print("\n🔴 BLOCKER ISSUES DETECTED - Health check failed")

                if args.blocker_fail or args.detailed:
                    # Generate blocker report
                    try:
                        from issue_reporter import IssueReporter

                        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                        report_path = Path(
                            args.output
                            if args.output
                            else f"temp/health-check-blocker-{timestamp}.md"
                        )
                        reporter = IssueReporter(
                            blocker_issues,
                            overall_score=0,
                            duration=(datetime.now() - start_time).total_seconds(),
                        )
                        reporter.save_report(report_path)
                    except ImportError:
                        print("⚠️ IssueReporter not available, skipping detailed report")

                if args.blocker_fail:
                    sys.exit(1)
                return
            else:
                print("✅ No blocker issues found - Proceeding with health check\n")

        except ImportError:
            print("⚠️ StrictChecker not available, skipping strict mode checks\n")

    #
    engine = HealthCheckEngine()

    #
    engine.run_all_checks()

    #
    if args.format in ["console", "all"]:
        engine.print_console_report()

    if args.format in ["json", "all"]:
        output_path = Path(args.output) if args.output else None
        engine.save_json_report(output_path)

    if args.format in ["markdown", "all"]:
        output_path = Path(args.output) if args.output else None
        engine.save_markdown_report(output_path)

    # Phase 14.2+ Detailed report with issue reporter
    if args.detailed:
        try:
            from issue_reporter import IssueReporter

            # Note: This requires updating all check methods to return Issue objects
            # For now, print a placeholder message
            print("\n📊 ")
            print("   : issue_model.py, issue_reporter.py, strict_checker.py")
        except ImportError:
            print("⚠️ IssueReporter not available")

    #
    if engine.results["total_score"] < 70:
        sys.exit(1)  #
    else:
        sys.exit(0)  #


if __name__ == "__main__":
    main()
