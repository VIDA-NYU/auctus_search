from typing import Callable, List, Union
import geopandas
import pandas
import ipywidgets as interactive_widgets
from beartype import beartype
from IPython.display import display


@beartype
class SpatialDatasetConverter:
    def __init__(
        self,
        dataset: Union[pandas.DataFrame, geopandas.GeoDataFrame],
        coordinate_reference_system: str,
        on_conversion_complete: Callable[[str, str, geopandas.GeoDataFrame], None],
    ) -> None:
        self.dataset: Union[pandas.DataFrame, geopandas.GeoDataFrame] = dataset
        self.coordinate_reference_system: str = coordinate_reference_system
        self.on_conversion_complete: Callable[
            [str, str, geopandas.GeoDataFrame], None
        ] = on_conversion_complete
        self._build_conversion_ui()

    def _build_conversion_ui(self) -> None:
        column_options: List[str] = ["None"] + list(self.dataset.columns)
        self.spatial_information_label: interactive_widgets.Label = (
            interactive_widgets.Label(
                value="➡️ Provide spatial attributes:",
                layout=interactive_widgets.Layout(margin="10px 0"),
            )
        )
        self.spatial_information_label.style.font_size = "16px"

        self.latitude_dropdown_widget: interactive_widgets.Dropdown = (
            interactive_widgets.Dropdown(
                options=column_options, description="Latitude:"
            )
        )
        self.longitude_dropdown_widget: interactive_widgets.Dropdown = (
            interactive_widgets.Dropdown(
                options=column_options, description="Longitude:"
            )
        )
        self.confirm_conversion_button: interactive_widgets.Button = (
            interactive_widgets.Button(description="Convert", button_style="success")
        )
        self.confirm_conversion_button.on_click(self._on_confirm_conversion)

        display(
            interactive_widgets.VBox(
                [
                    self.spatial_information_label,
                    self.latitude_dropdown_widget,
                    self.longitude_dropdown_widget,
                    self.confirm_conversion_button,
                ]
            )
        )

    def _on_confirm_conversion(self, button: interactive_widgets.Button) -> None:
        _ = button
        if (
            self.latitude_dropdown_widget.value == "None"
            or self.longitude_dropdown_widget.value == "None"
        ):
            self.spatial_information_label.value = (
                "Latitude and Longitude must be selected. Skipping conversion."
            )
            return

        latitude_column, longitude_column = (
            self.latitude_dropdown_widget.value,
            self.longitude_dropdown_widget.value,
        )

        temporary_copy_dataset = self.dataset.copy()
        self.dataset = geopandas.GeoDataFrame(
            temporary_copy_dataset,
            geometry=geopandas.points_from_xy(
                temporary_copy_dataset[longitude_column],
                temporary_copy_dataset[latitude_column],
            ),
            crs=self.coordinate_reference_system,
        )

        self.on_conversion_complete(latitude_column, longitude_column, self.dataset)
        self.spatial_information_label.value = f"Spatial attributes added successfully. Latitude: {latitude_column}, Longitude: {longitude_column}"
