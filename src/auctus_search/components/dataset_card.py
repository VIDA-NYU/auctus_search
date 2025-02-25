import re
from datetime import datetime
from typing import Callable, Dict
from typing import Optional
from typing import Union

import ipywidgets as widgets
from beartype import beartype
from millify import millify

from auctus_search.API.models import Dataset


@beartype
class AuctusDatasetCard:
    def __init__(
        self,
        dataset: Dataset,
        select_callback_function: Optional[Callable[[Dataset], None]] = None,
        style_overrides: Optional[Dict[str, Dict[str, str]]] = None,
    ) -> None:
        self.dataset: Dataset = dataset
        self.select_callback_function: Optional[Callable[[Dataset], None]] = (
            select_callback_function
        )
        self.style_overrides: Dict[str, Dict[str, str]] = (
            style_overrides if style_overrides is not None else {}
        )
        self._initialise_select_button()

    def _initialise_select_button(self) -> None:
        self.select_dataset_button: widgets.Button = widgets.Button(
            description="Select This Dataset",
            layout=widgets.Layout(
                width="100%", height="40px", border="none", border_radius="50px"
            ),
            button_style="",
            tooltip="Click to select this dataset",
        )
        default_button_styles: Dict[str, str] = {
            "button_color": "white",
            "font_size": "14px",
            "font_weight": "bold",
            "text_color": "#007AFF",
        }
        button_style_overrides: Dict[str, str] = self.style_overrides.get("button", {})
        merged_button_styles: Dict[str, str] = {
            **default_button_styles,
            **button_style_overrides,
        }
        for style_property, style_value in merged_button_styles.items():
            setattr(self.select_dataset_button.style, style_property, style_value)
        self.select_dataset_button.on_click(self._on_select_button_click)

    def _on_select_button_click(self, button: widgets.Button) -> None:
        _ = button
        if self.select_callback_function:
            self.select_callback_function(self.dataset)

    def _get_component_style(
        self, component_key: str, default_styles: Dict[str, str]
    ) -> str:
        style_overrides: Dict[str, str] = self.style_overrides.get(component_key, {})
        merged_styles: Dict[str, str] = {**default_styles, **style_overrides}
        return "; ".join(
            f"{style_property}: {style_value}"
            for style_property, style_value in merged_styles.items()
        )

    def _render_dataset_title(self) -> str:
        title_style: str = self._get_component_style(
            "title",
            {
                "margin": "0 0 2px 0",
                "font-size": "24px",
                "font-weight": "700",
                "color": "#333",
            },
        )
        name = self.dataset.metadata.name or "Unknown Name"
        return f'<h3 style="{title_style}">{name}</h3>'

    def _render_dataset_source_link(self) -> str:
        paragraph_style: str = self._get_component_style(
            "source_paragraph",
            {"font-size": "15px", "color": "#007aff", "margin": "2px 0"},
        )
        anchor_style: str = self._get_component_style(
            "source_anchor", {"text-decoration": "none", "color": "#007aff"}
        )
        source_url = self.dataset.metadata.source or "#"
        if not source_url.startswith(("http://", "https://")):
            source_url = "https://" + source_url
        return f'<p style="{paragraph_style}"><a href="{source_url}" target="_blank" style="{anchor_style}">{source_url}</a></p>'

    def _render_dataset_description(self) -> str:
        description_style: str = self._get_component_style(
            "description",
            {
                "font-size": "12px",
                "color": "#666",
                "margin": "2px 0 0 0",
                "max-height": "150px",
                "overflow-y": "scroll",
                "line-height": "20px",
                "padding-right": "10px",
                "text-align": "justify",
                "word-wrap": "break-word",
                "width": "100%",
            },
        )
        description = self.dataset.metadata.description or "No description available."

        cleaned_description = re.sub(r"\s+", " ", description).strip()
        cleaned_description = re.sub(r"[\"\'“”]", "", cleaned_description)

        url_pattern = r"(https?://[^\s]+)"
        clickable_description = re.sub(
            url_pattern,
            r'<a href="\1" target="_blank" style="color: #007aff; text-decoration: none;">\1</a>',
            cleaned_description,
        )

        return f'<p style="{description_style}">{clickable_description}</p>'

    def _render_tag(
        self,
        tag_label: str,
        primary_value: str,
        additional_info: str,
        tag_position: str,
    ) -> str:
        default_tag_styles = {
            "border-radius": "15px",
            "background-color": "white",
            "box-shadow": "0px 2px 16px rgba(0, 0, 0, 0.15)",
            "width": "110px",
            "height": "55px",
            "display": "grid",
            "grid-template-rows": "1fr 2fr 1fr",
            "justify-items": "center",
            "align-items": "center",
            "text-align": "center",
            "font-weight": "700",
            "z-index": "10",
        }
        tag_container_style = (
            f"position: absolute; {tag_position}; "
            + self._get_component_style("tag", default_tag_styles)
        )
        tag_label_style = self._get_component_style(
            "tag_label",
            {
                "font-size": "8px",
                "color": "rgba(0, 0, 0, 0.3)",
                "margin-bottom": "-10px",
            },
        )
        tag_value_style = self._get_component_style(
            "tag_value", {"font-size": "14px", "color": "#007AFF", "margin": "-10px 0"}
        )
        additional_info_style = self._get_component_style(
            "additional_info",
            {"font-size": "8px", "color": "#007AFF", "margin-top": "-10px"},
        )
        return f'''
        <div style="{tag_container_style}">
            <span style="{tag_label_style}">{tag_label}</span>
            <span style="{tag_value_style}">{primary_value}</span>
            <span style="{additional_info_style}">{additional_info}</span>
        </div>
        '''

    def _render_relevancy_gauge(self) -> str:
        gauge_container_style: str = self._get_component_style(
            "relevancy_gauge_container",
            {
                "position": "absolute",
                "bottom": "30px",
                "left": "50%",
                "transform": "translateX(-50%)",
                "width": "72px",
                "height": "72px",
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "background": "white",
                "border-radius": "50%",
                "box-shadow": "0px 2px 16px rgba(0, 0, 0, 0.15)",
                "z-index": "10",
            },
        )
        relevancy_score = round(self.dataset.score, 2)
        gauge_dash_offset: float = 251 - (relevancy_score / 100) * 251
        return f'''
        <div style="{gauge_container_style}">
            <svg width="72" height="72" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="#EEE" stroke-width="10" fill="none"/>
                <circle cx="50" cy="50" r="40" stroke="#007AFF" stroke-width="10" fill="none"
                    stroke-dasharray="251" stroke-dashoffset="{gauge_dash_offset}" transform="rotate(-90,50,50)"/>
                <text x="50" y="55" font-size="16" font-weight="bold" text-anchor="middle" fill="#007AFF">
                    {relevancy_score}%
                </text>
            </svg>
        </div>
        '''

    def _render_relevancy_label(self) -> str:
        relevancy_label_style: str = self._get_component_style(
            "relevancy_label",
            {
                "position": "absolute",
                "bottom": "0px",
                "left": "50%",
                "transform": "translateX(-50%)",
                "font-size": "8px",
                "font-weight": "700",
                "color": "rgba(0, 0, 0, 0.3)",
                "z-index": "10",
            },
        )
        return f'<p style="{relevancy_label_style}">Relevancy</p>'

    def _render_dataset_date(self) -> str:
        date_str = self.dataset.metadata.date or "N/A"
        if date_str != "N/A":
            try:
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                formatted_date = dt.strftime("%B %d, %Y")
            except ValueError:
                formatted_date = "Invalid date"
        else:
            formatted_date = "N/A"
        date_style: str = self._get_component_style(
            "date",
            {"font-size": "12px", "color": "#999", "margin": "2px 0"},
        )
        return f'<p style="{date_style}">Upload date: {formatted_date}</p>'

    @staticmethod
    def _format_dataset_size(dataset_size_value: Union[int, str]) -> str:
        try:
            dataset_size_integer: int = int(dataset_size_value)
        except (ValueError, TypeError):
            return "N/A"
        return millify(dataset_size_integer, precision=0)

    def render(self) -> widgets.VBox:
        card_style = self._get_component_style(
            "card",
            {
                "border-radius": "21px",
                "box-shadow": "0 4px 10px rgba(0,0,0,0.1)",
                "padding": "20px",
                "margin": "10px",
                "width": "338px",
                "height": "354px",
                "background-color": "#ffffff",
                "display": "flex",
                "flex-direction": "column",
                "font-family": "'SF Pro', Arial, sans-serif",
                "position": "relative",
                "overflow": "hidden",
            },
        )

        dataset_types = self.dataset.metadata.types or ["Unknown"]
        primary_type = (
            "Spatial"
            if "spatial" in [t.lower() for t in dataset_types]
            else dataset_types[0].capitalize()
        )
        additional_types = [
            t.capitalize() for t in dataset_types if t.lower() != primary_type.lower()
        ]
        type_additional_info = ""
        if additional_types:
            type_additional_info = f'<span style="cursor: pointer;" title="{", ".join(additional_types)}">{len(additional_types)} more</span>'

        dataset_size = self.dataset.metadata.nb_rows or "N/A"
        formatted_dataset_size = self._format_dataset_size(dataset_size)
        columns_info = ""
        if hasattr(self.dataset.metadata, "columns") and isinstance(
            self.dataset.metadata.columns, list
        ):
            num_columns = len(self.dataset.metadata.columns)
            column_names = [
                col.get("name", "Unknown")
                for col in self.dataset.metadata.columns
                if isinstance(col, dict)
            ]
            columns_info = (
                f'<span style="cursor: pointer;" title="{", ".join(column_names)}">{num_columns} columns</span>'
                if column_names
                else f"{num_columns} columns"
            )

        card_html = f'''
        <div style="{card_style}">
            {self._render_dataset_title()}
            {self._render_dataset_source_link()}
            {self._render_dataset_date()}
            {self._render_dataset_description()}
            {self._render_tag("Type", primary_type, type_additional_info, "bottom: 20px; left: 15px")}
            {self._render_tag("Size", formatted_dataset_size, columns_info, "bottom: 20px; right: 15px")}
            {self._render_relevancy_gauge()}
            {self._render_relevancy_label()}
        </div>
        '''
        card_widget = widgets.HTML(value=card_html)
        return widgets.VBox([card_widget, self.select_dataset_button])
