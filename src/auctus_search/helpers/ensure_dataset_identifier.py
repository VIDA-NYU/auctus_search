import functools
from typing import Callable, Any

from beartype import beartype


@beartype
def ensure_dataset_identifier(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        if not getattr(self, "selected_dataset_identifier", None):
            raise ValueError(
                "No dataset identifier found. Please search and select a dataset first."
            )
        return func(self, *args, **kwargs)

    return wrapper
