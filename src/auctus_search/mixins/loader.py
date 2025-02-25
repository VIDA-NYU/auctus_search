from typing import Any, Optional, Union
import io
import pandas
import geopandas
import requests
from beartype import beartype
from auctus_search.API import AuctusAPI
from auctus_search.helpers.ensure_dataset_identifier import ensure_dataset_identifier
from auctus_search.mixins import AuctusSearchDisplayMixin
from auctus_search.mixins.search import AuctusSearchMixin


@beartype
class AuctusSearchLoaderMixin:
    FILE_LOADER_FACTORY = {
        "csv": lambda content: pandas.read_csv(io.BytesIO(content)),
    }

    def __init__(self: "AuctusSearchMixin") -> None:
        self.current_selected_dataset: Optional[
            Union[pandas.DataFrame, geopandas.GeoDataFrame]
        ] = None

    @beartype
    def load_selected_dataset(
        self: Union["AuctusSearchLoaderMixin", "AuctusSearchMixin"],
        display_table: bool = True,
    ) -> Union[pandas.DataFrame, geopandas.GeoDataFrame]:
        dataset = self._load_dataset(self.selected_dataset_identifier)
        if dataset is None:
            raise ValueError(
                "No dataset loaded! Search & Select then you can load selected dataset."
            )
        if display_table:
            self._show_dataset(dataset)
        return dataset

    @ensure_dataset_identifier
    @beartype
    def _load_dataset(
        self, dataset_identifier: Any, dataset_format: str = "csv"
    ) -> Optional[Union[pandas.DataFrame, geopandas.GeoDataFrame]]:
        response = requests.get(AuctusAPI.download(dataset_identifier, dataset_format))
        response.raise_for_status()

        loader_func = self.FILE_LOADER_FACTORY.get(dataset_format)
        if loader_func is None:
            raise ValueError(
                f"Unsupported format '{dataset_format}'. "
                f"Supported formats: {list(self.FILE_LOADER_FACTORY.keys())}"
            )

        self.current_selected_dataset = loader_func(response.content)
        return self.current_selected_dataset

    @beartype
    def _show_dataset(
        self: "AuctusSearchDisplayMixin",
        dataset: Union[pandas.DataFrame, geopandas.GeoDataFrame],
    ) -> None:
        self.interactive_table_display(dataset)
