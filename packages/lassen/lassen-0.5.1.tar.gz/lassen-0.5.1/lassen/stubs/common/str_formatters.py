import ast
import enum
import inspect
from collections import deque
from typing import Any, Callable


def is_lambda(v):
    LAMBDA = lambda: 0  # noqa

    return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__


def get_lambda_body(func: Callable) -> str:
    func_lines, start_number = inspect.getsourcelines(func)
    func_range = set(range(start_number, start_number + len(func_lines)))

    file_path = inspect.getsourcefile(func)
    if not file_path:
        raise ValueError("Could not find source file for provided lambda.")
    with open(file_path, "r") as file:
        file_content = file.read()
    module = ast.parse(file_content)

    found_lambds: list[Any] = []
    todo: Any = deque([module])

    while todo:
        node = todo.popleft()
        # Only consider the outermost Lambda function, in the case of nested functions
        if isinstance(node, ast.Lambda):
            if node.lineno in func_range:
                found_lambds.append(node)
        else:
            todo.extend(ast.iter_child_nodes(node))

    if found_lambds:
        if len(found_lambds) > 1:
            raise ValueError(
                f"Multiple lambda functions found on the same line: {func_lines}"
            )
        return ast.unparse(found_lambds[0].body).strip()

    raise ValueError("No lambda function found in provided function.")


def format_function_args(args: list[str], kwargs: dict[str, Any]):
    """
    Args are inserted 1:1, kwargs are processed according to the
    format_dict_as_kwargs rules

    """
    all_args = args + [format_dict_as_kwargs(kwargs)]
    all_args = [arg for arg in all_args if arg.strip()]
    return ", ".join(all_args)


def format_dict_as_kwargs(dictionary: dict[str, Any]):
    """
    Formats a dictionary as keyword arguments. If a dictionary value is
    a lambda function, will attempt to extract its value as a string.

    """
    # These representations can be explicitly cast
    # Everything else should be in a lambda
    allowed_representations = (str, int, float, bool, type(None))
    representation_dict: dict[str, str] = {}

    def convert_value(value: Any):
        if isinstance(value, enum.Enum):
            return f"{value.__class__.__name__}.{value.name}"
        elif is_lambda(value):
            return f"lambda: {get_lambda_body(value)}"
        elif isinstance(value, list):
            # Convert the args
            converted_args: list[str] = [convert_value(arg) for arg in value]
            return f"[{', '.join(converted_args)}]"
        elif isinstance(value, allowed_representations):
            # Allowed representation fallback should be the last in the chain, since
            # these classes might be superclasses of other more specific targeting
            # (StrEnum, for instance) that we would rather process by their
            # targeted handler
            return repr(value)
        else:
            raise ValueError(
                f"Value {value} is not a valid default; cast with `lambda` in your"
                " code to maintain its representation."
            )

    for key, value in dictionary.items():
        representation_dict[key] = convert_value(value)

    return ", ".join(f"{k}={v}" for k, v in representation_dict.items())
