from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

PACKAGE = "instrument_harness_lab"

ALLOWED_INTERNAL_IMPORTS: dict[str, set[str]] = {
    "domain": set(),
    "instrument": {"domain"},
    "calibration": {"domain"},
    "controller": {"domain", "instrument", "calibration"},
    "cli": {"controller"},
}


@dataclass(frozen=True)
class ArchitectureViolation:
    file: Path
    imported_module: str
    message: str


def check_architecture(src_root: Path) -> list[ArchitectureViolation]:
    package_root = src_root / PACKAGE
    violations: list[ArchitectureViolation] = []
    for module_name, allowed_imports in ALLOWED_INTERNAL_IMPORTS.items():
        file_path = package_root / f"{module_name}.py"
        imported_modules = _internal_imports(file_path)
        for imported_module in imported_modules:
            if imported_module not in allowed_imports:
                violations.append(
                    ArchitectureViolation(
                        file=file_path,
                        imported_module=imported_module,
                        message=(
                            f"{module_name}.py must not import {PACKAGE}.{imported_module}; "
                            f"allowed imports: {sorted(allowed_imports)}"
                        ),
                    )
                )
    return violations


def _internal_imports(file_path: Path) -> set[str]:
    tree = ast.parse(file_path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.update(_project_module_parts(node.module))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.update(_project_module_parts(alias.name))
    return imports


def _project_module_parts(module_name: str) -> set[str]:
    prefix = f"{PACKAGE}."
    if not module_name.startswith(prefix):
        return set()
    module_tail = module_name.removeprefix(prefix)
    return {module_tail.split(".", maxsplit=1)[0]}
