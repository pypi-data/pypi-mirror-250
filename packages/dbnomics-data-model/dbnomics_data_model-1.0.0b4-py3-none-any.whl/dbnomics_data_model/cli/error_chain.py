from textwrap import indent

from dbnomics_data_model.errors import DataModelError


def format_error(error: BaseException) -> str:
    error_cls = type(error)
    error_cls_name = error_cls.__name__ if isinstance(error, DataModelError) else error_cls.__qualname__
    return f"{error_cls_name}: {error}"


def format_error_chain(error: Exception) -> str:
    """Format the error chain with all causes as a tree."""
    depth = 0
    text = format_error(error)
    current_error: BaseException = error

    while True:
        cause = current_error.__cause__
        if cause is None:
            break
        current_error = cause
        depth += 1
        text += "\n" + indent(format_error(current_error), " " * 2 * depth)

    return text
