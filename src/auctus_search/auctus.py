import io
import json
from typing import Any, Dict, List, Optional, Union, Callable
import geopandas
import ipywidgets as interactive_widgets
import pandas
import requests
from IPython.display import display, clear_output
from beartype import beartype
from ipywidgets import GridspecLayout, Output
from .API import AuctusAPI
from .components import AuctusDatasetCard
from .components.spatial_dataset_converter import (
    SpatialDatasetConverter,
)
from skrub import TableReport
from IPython.display import display, HTML


def show_table(
        dataframe: Union[pandas.DataFrame, geopandas.GeoDataFrame],
        n_rows: int = 10,
        order_by: Optional[Union[str, List[str]]] = None,
        title: Optional[str] = "Table Report",
        column_filters: Optional[Dict[str, Dict[str, Union[str, List[str]]]]] = None,
        verbose: int = 1,
) -> None:
    if dataframe is not None and 0 < n_rows < len(dataframe):
        report = TableReport(
            dataframe=dataframe,
            n_rows=n_rows,
            order_by=order_by,
            title=title,
            column_filters=column_filters,
            verbose=verbose,
        )
        display(HTML(report.html()))


@beartype
class AuctusSearch:
    def __init__(self, coordinate_reference_system: str = "EPSG:4326") -> None:
        self.selected_dataset_identifier: Optional[Any] = None
        self.selected_dataset_name: Optional[str] = None
        self.current_selected_dataset: Optional[
            Union[pandas.DataFrame, geopandas.GeoDataFrame]
        ] = None
        self.current_selected_latitude_column: Optional[str] = None
        self.current_selected_longitude_column: Optional[str] = None
        self.selection_label_widget: interactive_widgets.Label = (
            interactive_widgets.Label(
                value="", layout=interactive_widgets.Layout(margin="10px 0")
            )
        )
        self.selection_label_widget.style.font_size = "20px"
        self.output_area_widget: Output = Output()
        self.coordinate_reference_system: str = coordinate_reference_system

    def search_datasets(
        self, search_query: Union[str, List[str]]
    ) -> List[Dict[str, Any]]:
        self._clear_selected_dataset_label()
        query_payload: Dict[str, Any] = (
            {"keywords": search_query.split()}
            if isinstance(search_query, str)
            else {"keywords": search_query}
        )
        response: requests.Response = requests.post(
            AuctusAPI.search(), data={"query": json.dumps(query_payload)}
        )
        response.raise_for_status()
        results: List[Dict[str, Any]] = response.json().get("results", [])
        self._render_results(results)
        return results

    def select_dataset(self) -> None:
        dataset: Optional[Union[pandas.DataFrame, geopandas.GeoDataFrame]] = (
            self.load_dataset(self.selected_dataset_identifier)
        )
        if dataset is not None:
            show_table(dataset)
        else:
            raise ValueError("No dataset loaded! Select and load a dataset first.")

    def load_dataset(
        self, dataset_identifier: Any, dataset_format: str = "csv"
    ) -> Optional[Union[pandas.DataFrame, geopandas.GeoDataFrame]]:
        if not dataset_identifier:
            raise ValueError("Error loading dataset.")
        response: requests.Response = requests.get(
            AuctusAPI.download(dataset_identifier, dataset_format)
        )
        response.raise_for_status()
        if dataset_format == "csv":
            self.current_selected_dataset = pandas.read_csv(
                io.BytesIO(response.content)
            )
        else:
            raise ValueError("Unsupported format. Only 'csv' is allowed for now. ")
        return self.current_selected_dataset

    def convert_to_spatial_dataset(
        self,
        callback: Optional[Callable[[str, str, geopandas.GeoDataFrame], None]] = None,
    ) -> None:
        if self.current_selected_dataset is None:
            raise ValueError("No dataset loaded! Select and load a dataset first.")

        def wrapped_callback(
            latitude_column: str,
            longitude_column: str,
            converted_dataset: geopandas.GeoDataFrame,
        ) -> None:
            self._on_spatial_conversion_complete(
                latitude_column, longitude_column, converted_dataset
            )
            if callback:
                callback(latitude_column, longitude_column, converted_dataset)

        SpatialDatasetConverter(
            dataset=self.current_selected_dataset,
            coordinate_reference_system=self.coordinate_reference_system,
            on_conversion_complete=wrapped_callback,
        )

    def _on_spatial_conversion_complete(
        self,
        latitude_column: str,
        longitude_column: str,
        converted_dataset: geopandas.GeoDataFrame,
    ) -> None:
        self.current_selected_latitude_column = latitude_column
        self.current_selected_longitude_column = longitude_column
        self.current_selected_dataset = converted_dataset

    def _set_selected_dataset_callback(
        self, dataset_identifier: Any, dataset_name: str
    ) -> None:
        self.selected_dataset_identifier = dataset_identifier
        self.selected_dataset_name = dataset_name
        self.selection_label_widget.value = f"Selected Dataset: {dataset_name}"

    def _clear_selected_dataset_label(self) -> None:
        self.selected_dataset_identifier = None
        self.selected_dataset_name = None
        self.selection_label_widget.value = ""

    def _render_results(self, dataset_results: List[Dict[str, Any]]) -> None:
        with self.output_area_widget:
            clear_output(wait=True)
            display(self.selection_label_widget)
            if not dataset_results:
                display(interactive_widgets.HTML("<h3>No datasets found.</h3>"))
            else:
                dataset_cards: List[interactive_widgets.Widget] = [
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
                display(dataset_grid)
        display(self.output_area_widget)
