import functools
from typing import Callable, Any

from beartype import beartype


@beartype
def ensure_dataset_loaded(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        if getattr(self, "current_selected_dataset", None) is None:
            raise ValueError("Dataset not loaded. Please load the dataset first.")
        return func(self, *args, **kwargs)

    return wrapper
