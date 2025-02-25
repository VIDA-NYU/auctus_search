import functools
from typing import Callable, Any

from beartype import beartype


@beartype
def ensure_non_empty_search_query(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self, search_query, *args, **kwargs) -> Any:
        if not search_query or (
            isinstance(search_query, str) and not search_query.strip()
        ):
            raise ValueError("Search query cannot be empty.")
        return func(self, search_query, *args, **kwargs)

    return wrapper
