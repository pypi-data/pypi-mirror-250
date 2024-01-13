import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Type

from inflection import underscore
from pydantic import BaseModel

if TYPE_CHECKING:
    from lassen.stubs.common import ExtractedStubImports


@dataclass
class RenderedFile:
    content: str
    created_classes: list[str]


def get_ordered_instance_variables(cls: type) -> list[str]:
    fields_ordered: list[str] = []

    # Recursively gather variables from the parent classes
    for parent in cls.__bases__:
        fields_ordered.extend(get_ordered_instance_variables(parent))

    # Fetch the variables from the model's class itself
    model_vars = [key for key in vars(cls).keys() if not key.startswith("__")]
    fields_ordered.extend(model_vars)

    return fields_ordered


class BaseDefinition(ABC, BaseModel):
    """
    A Definition can provide additional metadata to generators so they can implement
    their own parsing logic.
    """


class BaseStub(ABC):
    """
    A Stub is the core definition class that users leverage to define their data schema.
    It serves as the ground truth for the model that is used in the database and within
    most CRUD API endpoints that are fronting the database.
    """

    @classmethod
    def get_generators(cls) -> list["BaseGenerator"]:
        return [
            generator
            for _, generator in inspect.getmembers(
                cls, lambda m: isinstance(m, BaseGenerator)
            )
        ]

    @classmethod
    def ordered_instance_variables(cls):
        return get_ordered_instance_variables(cls)

    @classmethod
    def get_filename(cls):
        return underscore(cls.__name__)


class BaseGenerator(ABC):
    """
    A Generator takes input Stub definition and translates it to code definition files
    that will actually be used by the client application. They allow one stub file to
    be repurposed for Pydantic, SQLAlchemy, etc.
    """

    output_directory: str

    def __init__(self, output_directory: str):
        self.output_directory = output_directory

    @abstractmethod
    def __call__(
        self,
        model: Type[BaseStub],
        import_hints: "ExtractedStubImports",
        type_hints: dict[str, type],
    ) -> RenderedFile:
        pass
