import importlib
import inspect
import re
import typing

from neos_common import schema


def _is_neos_error_code(code: str) -> bool:
    m = re.match(r"^[A-Z]+\d{3}$", code)
    return bool(m)


def get_error_codes(module_names: typing.Union[str, typing.List[str]]) -> schema.ErrorCodes:
    """Get all error codes and messages from the error module."""
    errors = []

    if isinstance(module_names, str):
        module_names = [module_names]

    for module_name in module_names:
        module = importlib.import_module(module_name)

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                code = str(getattr(obj, "code", ""))
                message = getattr(obj, "message", "")

                if _is_neos_error_code(code):
                    errors.append(
                        schema.ErrorCode(
                            class_name=name,
                            code=code,
                            message=message,
                        ),
                    )

    return schema.ErrorCodes(errors=errors)
