from pathlib import Path
from typing import AsyncIterable, Iterable, TypeVar


def guess_package_location(required_subdirectory: str):
    """
    Traverse the current path up to root and look for a pyproject.toml file.
    Once found, search for a `required_subdirectory` directory in its main directories.
    This helps cut back on the false-positives of python directories that are located
    in the same root but not actually where we want to insert files.

    """
    current_path = Path.cwd()

    # Traverse the directory hierarchy up to the root
    while True:
        pyproject_path = current_path / "pyproject.toml"
        setup_path = current_path / "setup.py"
        if pyproject_path.exists() or setup_path.exists():
            # Found pyproject.toml, search for migrate directory in its main directories
            for child in current_path.iterdir():
                if child.is_dir() and (child / required_subdirectory).exists():
                    return child

        # Move up to the parent directory
        parent_path = current_path.parent
        if parent_path == current_path:
            # Reached the root directory, no pyproject.toml or migrate directory found
            raise ValueError("No pyproject.toml file found or migrate directory found.")

        current_path = parent_path


T = TypeVar("T")


def get_batch(iterable: Iterable[T], n: int) -> Iterable[list[T]]:
    """
    Yield successive n-sized chunks from iterable.
    """
    # Create an iterator from the iterable
    it = iter(iterable)

    chunk: list[T] = []

    for element in it:
        chunk.append(element)
        if len(chunk) == n:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


async def get_batch_async(iterable: AsyncIterable[T], n: int) -> AsyncIterable[list[T]]:
    chunk: list[T] = []

    async for element in iterable:
        chunk.append(element)
        if len(chunk) == n:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
