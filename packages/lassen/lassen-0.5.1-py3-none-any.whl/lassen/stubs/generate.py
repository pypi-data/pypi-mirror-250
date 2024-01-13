import importlib
import importlib.util
import inspect
import os
import pkgutil
import sys
from pathlib import Path
from typing import Type

from click import command, secho
from inflection import underscore

from lassen.constants import CLIENT_STUB_DIRECTORY
from lassen.io import guess_package_location
from lassen.stubs.base import BaseGenerator, BaseStub
from lassen.stubs.common import extract_stub_imports, get_resolved_type_hints


def generate_files() -> list[Type[BaseStub]]:
    root_path = guess_package_location(CLIENT_STUB_DIRECTORY)
    sys.path.append(os.path.dirname(root_path))

    stub_models: list[tuple[Type[BaseStub], Path]] = []

    package = importlib.import_module(root_path.name)

    # Assume the
    for _, module_name, _ in pkgutil.walk_packages(
        path=[root_path / CLIENT_STUB_DIRECTORY],
        prefix=package.__name__ + f".{CLIENT_STUB_DIRECTORY}.",
    ):
        definition_module = importlib.import_module(module_name)

        stub_models += [
            (val, Path(inspect.getfile(val)))
            for _, val in inspect.getmembers(
                definition_module,
                lambda x: inspect.isclass(x) and issubclass(x, BaseStub),
            )
            if val != BaseStub
        ]

    if not stub_models:
        secho(f"No stub models found, checked: {root_path}", fg="red")
        return []

    secho("Found stub models:", fg="blue")
    for model, path in stub_models:
        secho(f"  {model.__name__} ({path.name})", fg="blue")

    model_generators: list[tuple[Type[BaseStub], Path, list[BaseGenerator]]] = [
        (
            model,
            path,
            model.get_generators(),
        )
        for model, path in stub_models
    ]

    unique_generators = set(
        generator for _, _, generators in model_generators for generator in generators
    )

    # Set up the base folders
    # This includes a new __init__ stub in each directory that can be
    # used to import dependency files
    for generator in unique_generators:
        generator_output = root_path / generator.output_directory
        generator_output.mkdir(parents=True, exist_ok=True)

        # Clear the old files, since the user might have deleted the
        # underlying stubs in the meantime
        for file in generator_output.iterdir():
            if file.is_file():
                file.unlink()

        with open(generator_output / "__init__.py", "w") as f:
            f.write("")

    try:
        for model, path, generators in model_generators:
            # Extract the explicit import from the model and its user-defined parents
            # Skip the lassen-internal base class itself since this won't have any
            # imports that are relevant to the definitions
            parent_paths = [
                Path(inspect.getfile(model))
                for model in model.__bases__
                if model != BaseStub
            ]
            stub_imports = extract_stub_imports([path] + parent_paths)

            # Type resolution can only occur once we have loaded in
            # all of the models, since we need to resolve circular
            # dependencies through name definitions
            type_hints = get_resolved_type_hints(
                model,
                stub_models=[model for model, _ in stub_models],
                stub_imports=stub_imports,
            )

            secho(f"Generating files for {model.__name__}")

            for generator in generators:
                generator_output = root_path / generator.output_directory
                rendered = generator(
                    model, import_hints=stub_imports, type_hints=type_hints
                )
                with open(generator_output / f"{model.get_filename()}.py", "w") as f:
                    f.write(rendered.content)

                with open(generator_output / "__init__.py", "a") as f:
                    for created_class in rendered.created_classes:
                        f.write(
                            f"from .{underscore(model.__name__)}"
                            f" import {created_class} # noqa: F401\n"
                        )

            if generators:
                secho(f"Generated files for {model.__name__}", fg="green")
            else:
                secho(f"No generators found for {model.__name__}", fg="yellow")
    except Exception as e:
        secho("Exception encountered, cleaning up filesystem...", fg="red")

        for generator in unique_generators:
            generator_output = root_path / generator.output_directory
            generator_output.mkdir(parents=True, exist_ok=True)

            # Clear the old files, since the user might have deleted the underlying
            # stubs in the meantime
            for file in generator_output.iterdir():
                if file.is_file():
                    file.unlink()

            with open(generator_output / "__init__.py", "w") as f:
                f.write("")

        raise e

    return [model for model, _ in stub_models]


@command()
def cli():
    generate_files()
