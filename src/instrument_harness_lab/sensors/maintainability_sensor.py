from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

MAX_FUNCTION_LINES = 45
MAX_BRANCH_NODES = 8


@dataclass(frozen=True)
class MaintainabilityViolation:
    file: Path
    line: int
    message: str


def check_maintainability(src_root: Path) -> list[MaintainabilityViolation]:
    violations: list[MaintainabilityViolation] = []
    for file_path in sorted(src_root.rglob("*.py")):
        tree = ast.parse(file_path.read_text(encoding="utf-8"))
        violations.extend(_check_functions(file_path, tree))
        violations.extend(_check_print_boundary(file_path, tree))
    return violations


def _check_functions(file_path: Path, tree: ast.AST) -> list[MaintainabilityViolation]:
    violations: list[MaintainabilityViolation] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            function_length = (node.end_lineno or node.lineno) - node.lineno + 1
            if function_length > MAX_FUNCTION_LINES:
                violations.append(
                    MaintainabilityViolation(
                        file=file_path,
                        line=node.lineno,
                        message=f"{node.name} is {function_length} lines; split it below 45 lines",
                    )
                )
            branch_count = _branch_count(node)
            if branch_count > MAX_BRANCH_NODES:
                violations.append(
                    MaintainabilityViolation(
                        file=file_path,
                        line=node.lineno,
                        message=f"{node.name} has {branch_count} branch nodes; simplify the flow",
                    )
                )
    return violations


def _check_print_boundary(file_path: Path, tree: ast.AST) -> list[MaintainabilityViolation]:
    if file_path.name in {"cli.py", "run_feedback.py"}:
        return []

    violations: list[MaintainabilityViolation] = []
    for node in ast.walk(tree):
        is_print_call = (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "print"
        )
        if is_print_call:
            violations.append(
                MaintainabilityViolation(
                    file=file_path,
                    line=node.lineno,
                    message="only cli.py may print user-facing output",
                )
            )
    return violations


def _branch_count(node: ast.AST) -> int:
    branch_types = (ast.If, ast.For, ast.While, ast.Try, ast.Match, ast.BoolOp, ast.IfExp)
    return sum(1 for child in ast.walk(node) if isinstance(child, branch_types))
