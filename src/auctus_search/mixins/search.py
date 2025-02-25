from auctus_search.API.collection import DatasetCollection
from auctus_search.API.models import Dataset, Metadata
import dataclasses
import json
from typing import Any, Dict, List, Optional, Union

import ipywidgets as widgets
import requests
from IPython.display import clear_output, display
from ipywidgets import GridspecLayout, Output

from auctus_search.API import AuctusAPI
from auctus_search.components import AuctusDatasetCard
from auctus_search.helpers.ensure_non_empty_search_query import (
    ensure_non_empty_search_query,
)

from beartype import beartype


@beartype
class AuctusSearchMixin:
    def __init__(self) -> None:
        self.selected_dataset: Optional[Dataset] = None
        self.selected_dataset_identifier: Optional[Any] = None
        self.selected_dataset_name: Optional[str] = None
        self.selection_label_widget: widgets.Label = widgets.Label(
            value="", layout=widgets.Layout(margin="10px 0")
        )
        self.selection_label_widget.style.font_size = "20px"
        self.output_area_widget: Output = Output()
        self.search_query: Optional[str, List[str]] = None

    @ensure_non_empty_search_query
    @beartype
    def search_datasets(
        self,
        search_query: Union[str, List[str]],
        page: int = 1,
        size: int = 10,
        display_initial_results: bool = False,
    ) -> DatasetCollection:
        self._clear_selected_dataset_label()
        self.search_query = search_query

        query_payload: Dict[str, Any] = (
            {"keywords": search_query.split()}
            if isinstance(search_query, str)
            else {"keywords": search_query}
        )
        response: requests.Response = requests.post(
            AuctusAPI.search(),
            params={"page": page, "size": size},
            data={"query": json.dumps(query_payload)},
        )
        response.raise_for_status()
        raw_results: List[Dict[str, Any]] = response.json().get("results", [])
        datasets = []
        for result in raw_results:
            metadata_dict = result.get("metadata", {})
            metadata_fields = {
                field.name: metadata_dict.get(field.name)
                for field in dataclasses.fields(Metadata)
            }
            metadata = Metadata(**metadata_fields)
            dataset = Dataset(
                id=result.get("id"), score=result.get("score", 0.0), metadata=metadata
            )
            datasets.append(dataset)
        datasets_collection = DatasetCollection(datasets, self)
        if display_initial_results:
            self._render_results(datasets_collection.datasets)
        return datasets_collection

    @beartype
    def _clear_selected_dataset_label(self) -> None:
        self.selected_dataset = None
        self.selected_dataset_identifier = None
        self.selected_dataset_name = None
        self.selection_label_widget.value = ""

    @beartype
    def _set_selected_dataset_callback(self, dataset: Dataset) -> None:
        self.selected_dataset = dataset
        self.selected_dataset_identifier = dataset.id
        self.selected_dataset_name = dataset.metadata.name or "Unknown Name"
        self.selection_label_widget.value = (
            f"⏭️Selected Dataset: {self.selected_dataset_name}"
        )

    @beartype
    def _render_results(self, dataset_results: List[Dataset]) -> None:
        with self.output_area_widget:
            clear_output(wait=True)
            display(self.selection_label_widget)
            if dataset_results:
                dataset_cards: List[widgets.Widget] = [
                    AuctusDatasetCard(
                        dataset_result,
                        select_callback_function=self._set_selected_dataset_callback,
                    ).render()
                    for dataset_result in dataset_results
                ]
                dataset_grid: GridspecLayout = GridspecLayout(
                    (len(dataset_cards) // 3) + (len(dataset_cards) % 3 > 0), 3
                )
                for index, dataset_card in enumerate(dataset_cards):
                    dataset_grid[index // 3, index % 3] = dataset_card

                centered_grid = widgets.HBox(
                    [dataset_grid],
                    layout=widgets.Layout(
                        justify_content="center",
                        padding="10px",
                        width="100%",
                    ),
                )
                display(centered_grid)
            else:
                display(widgets.HTML("<h3>No datasets found.</h3>"))
        display(self.output_area_widget)
