from typing import List, Callable, Any, Union

from beartype import beartype

from auctus_search.API.models import Dataset

from functools import wraps


def ensure_metadata_fields(fields: List[str]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for dataset in self.datasets:
                for field in fields:
                    if field == "score":
                        if not hasattr(dataset, "score"):
                            raise ValueError(
                                f"Dataset {dataset.id} is missing 'score'."
                            )
                    else:
                        if not hasattr(dataset.metadata, field):
                            raise ValueError(
                                f"Dataset {dataset.id} is missing metadata field '{field}'."
                            )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


@beartype
class DatasetCollection:
    def __init__(
        self, datasets: List[Dataset], auctus_search, filters: List[str] = None
    ):
        self.datasets = datasets
        self.auctus_search = auctus_search
        self.filters = filters or []

    def _filter(
        self, condition: Callable[[Dataset], bool], filter_name: str, filter_value: Any
    ):
        filtered_datasets = [dataset for dataset in self.datasets if condition(dataset)]
        new_filters = self.filters + [f"{filter_name}: {filter_value}"]
        return DatasetCollection(filtered_datasets, self.auctus_search, new_filters)

    @ensure_metadata_fields(["types"])
    @beartype
    def with_types(self, types: List[str]):
        return self._filter(
            lambda dataset: any(
                type_.lower() in dataset.metadata.types for type_ in types
            ),
            "with_types",
            types,
        )

    @ensure_metadata_fields(["nb_rows"])
    @beartype
    def with_number_of_rows_greater_than(self, min_rows: int):
        return self._filter(
            lambda dataset: dataset.metadata.nb_rows is not None
            and dataset.metadata.nb_rows > min_rows,
            "with_number_of_rows_greater_than",
            min_rows,
        )

    @ensure_metadata_fields(["nb_rows"])
    @beartype
    def with_number_of_rows_less_than(self, max_rows: int):
        return self._filter(
            lambda dataset: dataset.metadata.nb_rows is not None
            and dataset.metadata.nb_rows < max_rows,
            "with_number_of_rows_less_than",
            max_rows,
        )

    @ensure_metadata_fields(["nb_rows"])
    @beartype
    def with_number_of_rows_between(self, min_rows: int, max_rows: int):
        return self._filter(
            lambda dataset: dataset.metadata.nb_rows is not None
            and min_rows <= dataset.metadata.nb_rows <= max_rows,
            "with_number_of_rows_between",
            (min_rows, max_rows),
        )

    @ensure_metadata_fields(["columns"])
    @beartype
    def with_number_of_columns_greater_than(self, min_columns: int):
        return self._filter(
            lambda dataset: len(dataset.metadata.columns) > min_columns,
            "with_number_of_columns_greater_than",
            min_columns,
        )

    @ensure_metadata_fields(["columns"])
    @beartype
    def with_number_of_columns_less_than(self, max_columns: int):
        return self._filter(
            lambda dataset: len(dataset.metadata.columns) < max_columns,
            "with_number_of_columns_less_than",
            max_columns,
        )

    @ensure_metadata_fields(["columns"])
    @beartype
    def with_number_of_columns_between(self, min_columns: int, max_columns: int):
        return self._filter(
            lambda dataset: min_columns <= len(dataset.metadata.columns) <= max_columns,
            "with_number_of_columns_between",
            (min_columns, max_columns),
        )

    @ensure_metadata_fields(["score"])
    @beartype
    def with_score_greater_than(self, min_score: Union[int, float]):
        return self._filter(
            lambda dataset: dataset.score > min_score,
            "with_score_greater_than",
            min_score,
        )

    @ensure_metadata_fields(["score"])
    @beartype
    def with_score_less_than(self, max_score: Union[int, float]):
        return self._filter(
            lambda dataset: dataset.score < max_score, "with_score_less_than", max_score
        )

    @ensure_metadata_fields(["score"])
    @beartype
    def with_score_between(
        self, min_score: Union[int, float], max_score: Union[int, float]
    ):
        return self._filter(
            lambda dataset: min_score <= dataset.score <= max_score,
            "with_score_between",
            (min_score, max_score),
        )

    @beartype
    def preview(self) -> None:
        steps = ["Dataset Collection Preview:", "├── Search Query: <Not Set>"]
        if self.auctus_search.search_query:
            steps[1] = f"├── Search Query: {self.auctus_search.search_query}"
        steps.append("├── Filters Applied:")
        if not self.filters:
            steps.append("│   └── None")
        else:
            for i, filter_info in enumerate(self.filters):
                if i == len(self.filters) - 1:
                    steps.append(f"│   └── {filter_info}")
                else:
                    steps.append(f"│   ├── {filter_info}")
        steps.append("└── Datasets Summary")
        if not self.datasets:
            steps.append("    └── No datasets found")
        else:
            steps.append(f"    └── {len(self.datasets)}")
        print("\n".join(steps))

    @beartype
    def display(self) -> None:
        self.auctus_search._render_results(self.datasets)
