from __future__ import annotations

import ast
from pathlib import Path


def test_application_does_not_define_schema_models() -> None:
    application_dir = Path(__file__).parents[1] / "application"

    invalid_defs: list[str] = []
    invalid_imports: list[str] = []

    for path in application_dir.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and any(
                _base_name(base) == "CyreneAISchema" for base in node.bases
            ):
                invalid_defs.append(f"{path.name}:{node.name}")
            if isinstance(node, ast.ImportFrom) and node.module == "pydantic":
                invalid_imports.append(f"{path.name}:pydantic")
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "pydantic":
                        invalid_imports.append(f"{path.name}:pydantic")

    assert invalid_defs == []
    assert invalid_imports == []


def test_application_does_not_import_infra() -> None:
    application_dir = Path(__file__).parents[1] / "application"

    invalid_imports: list[str] = []
    for path in application_dir.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module == "cyreneAI.infra" or node.module.startswith(
                    "cyreneAI.infra."
                ):
                    invalid_imports.append(f"{path.name}:{node.module}")
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "cyreneAI.infra" or alias.name.startswith(
                        "cyreneAI.infra."
                    ):
                        invalid_imports.append(f"{path.name}:{alias.name}")

    assert invalid_imports == []


def _base_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None
