import functools
import inspect
from typing import Callable

from beartype import beartype


@beartype
def check_dict_keys(param: str, keys: tuple) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            value = bound.arguments.get(param)
            if not isinstance(value, dict):
                raise ValueError(f"Parameter '{param}' must be a dict.")
            for key in keys:
                if key not in value:
                    raise ValueError(f"Parameter '{param}' must contain key '{key}'.")
            return func(*args, **kwargs)

        return wrapper

    return decorator
