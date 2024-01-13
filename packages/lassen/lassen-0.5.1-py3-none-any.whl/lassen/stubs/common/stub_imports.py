import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass
class SubImportDefinition:
    # Absolute imports from 3rd party packages
    module_name: str | None = None

    # Relative imports from local path
    module_path: Path | None = None

    # Specified in the `from` statement case. Direct imports are importing
    # an entire module so aren't relevant
    object_name: str | None = None


@dataclass
class ImportDefinition:
    definition: str
    module_definitions: list[SubImportDefinition]
    is_typechecking: bool = False


@dataclass
class ExtractedStubImports:
    clone_imports: list[ImportDefinition]
    clone_typechecking_imports: list[ImportDefinition]


def extract_stub_imports(path: Path | list[Path]):
    """
    Given a path, extract the import statements from its source file.

    This is used to clone imports from the original stub file in case they capture
    typehints that are not explicitly used in the model

    """
    if not isinstance(path, list):
        paths = [path]
    else:
        paths = path

    stub_imports: list[ImportDefinition] = []

    for path in paths:
        with open(path, "r") as file:
            file_content = file.read()
        module = ast.parse(file_content)

        # Ignore lassen imports by default, since this often brings in conflicting
        # type definitions
        stub_imports += [
            module_import
            for module_import in extract_imports(module, originating_file=path)
            if "lassen" not in module_import.definition
        ]

    return ExtractedStubImports(
        clone_imports=[
            import_def for import_def in stub_imports if not import_def.is_typechecking
        ],
        clone_typechecking_imports=[
            import_def for import_def in stub_imports if import_def.is_typechecking
        ],
    )


def extract_imports(
    node: Any, originating_file: Path, under_type_checking: bool = False
) -> Iterable[ImportDefinition]:
    if isinstance(node, ast.Import):
        definition = f"import {','.join([alias.name for alias in node.names])}"
        yield ImportDefinition(
            definition=definition,
            is_typechecking=under_type_checking,
            module_definitions=[
                SubImportDefinition(
                    module_name=alias.name,
                )
                for alias in node.names
            ],
        )
        return
    elif isinstance(node, ast.ImportFrom):
        imported_objects = ", ".join([alias.name for alias in node.names])
        level_dots = "." * node.level if node.level > 0 else ""
        definition = f"from {level_dots}{node.module} import {imported_objects}"

        # One . corresponds to a relative current path, and each additional
        # dot corresponds to a level up in the module path
        path_relative = ("../" * (node.level - 1)) if node.level > 0 else None

        yield ImportDefinition(
            definition=definition,
            is_typechecking=under_type_checking,
            module_definitions=[
                SubImportDefinition(
                    module_name=node.module if path_relative is None else None,
                    module_path=(
                        originating_file.parent
                        / path_relative
                        / node.module.replace(".", "/")
                    )
                    .resolve()
                    .with_suffix(".py")
                    if path_relative is not None and node.module
                    else None,
                    object_name=alias.name,
                )
                for alias in node.names
            ],
        )
        return
    elif (
        isinstance(node, ast.If)
        and isinstance(node.test, ast.Name)
        and node.test.id == "TYPE_CHECKING"
    ):
        for sub_node in node.body:
            yield from extract_imports(sub_node, originating_file, True)
    else:
        for sub_node in ast.iter_child_nodes(node):  # type: ignore
            yield from extract_imports(sub_node, originating_file, under_type_checking)
