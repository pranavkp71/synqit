from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class HeuristicResult:
    """Result of a heuristic check."""
    risk_level: str  # Low, Medium, High
    reason: str
    category: str


@dataclass
class Analysis:
    """Aggregated analysis results."""
    results: List[HeuristicResult] = field(default_factory=list)
    score: int = 0  # 0-100 risk score

    @property
    def max_risk(self) -> str:
        if any(r.risk_level == "High" for r in self.results):
            return "High"
        if any(r.risk_level == "Medium" for r in self.results):
            return "Medium"
        return "Low"


class HeuristicAnalyzer:
    """Analyze git diffs for common risks using simple heuristics."""

    AUTH_KEYWORDS = {
        "auth", "login", "session", "token", "password",
        "security", "middleware", "jwt", "cookie", "oauth"
    }

    ENV_KEYWORDS = {
        ".env", "config.py", "settings.py", "credentials", "secrets"
    }

    def __init__(self, diff: str, changed_files: List[str]):
        self.diff = diff
        self.changed_files = changed_files

    def analyze(self) -> Analysis:
        analysis = Analysis()

        # Run checks
        self._check_auth_changes(analysis)
        self._check_migrations(analysis)
        self._check_env_changes(analysis)
        self._check_missing_tests(analysis)
        self._check_large_deletions(analysis)

        # Calculate score (simple heuristic)
        high_risks = sum(1 for r in analysis.results if r.risk_level == "High")
        med_risks = sum(1 for r in analysis.results if r.risk_level == "Medium")
        analysis.score = min(100, (high_risks * 40) + (med_risks * 15))

        return analysis

    def _check_auth_changes(self, analysis: Analysis):
        for file in self.changed_files:
            file_lower = file.lower()
            if any(kw in file_lower for kw in self.AUTH_KEYWORDS):
                analysis.results.append(HeuristicResult(
                    risk_level="High",
                    category="Security",
                    reason=f"Sensitive authentication/security file modified: {file}"
                ))
                return # Only add once

    def _check_migrations(self, analysis: Analysis):
        if any("migrations" in file.lower() for file in self.changed_files):
            analysis.results.append(HeuristicResult(
                risk_level="Medium",
                category="Database",
                reason="Database migrations detected. Ensure backward compatibility."
            ))

    def _check_env_changes(self, analysis: Analysis):
        for file in self.changed_files:
            if any(kw in file.lower() for kw in self.ENV_KEYWORDS):
                analysis.results.append(HeuristicResult(
                    risk_level="High",
                    category="Config",
                    reason=f"Environment or configuration file changed: {file}"
                ))
                return

    def _check_missing_tests(self, analysis: Analysis):
        code_files = [
            f for f in self.changed_files 
            if f.endswith(".py") and "test" not in f.lower()
        ]
        test_files = [f for f in self.changed_files if "test" in f.lower()]

        if code_files and not test_files:
            analysis.results.append(HeuristicResult(
                risk_level="Medium",
                category="Testing",
                reason=f"Modified {len(code_files)} code files but no tests updated."
            ))

    def _check_large_deletions(self, analysis: Analysis):
        deleted_lines = len(re.findall(r"^\-", self.diff, re.MULTILINE))
        added_lines = len(re.findall(r"^\+", self.diff, re.MULTILINE))

        if deleted_lines > 50 and added_lines < (deleted_lines / 2):
            reason = (
                f"Large deletion detected ({deleted_lines} lines). "
                "Verify no functionality was lost."
            )
            analysis.results.append(HeuristicResult(
                risk_level="Medium",
                category="Risk",
                reason=reason
            ))
