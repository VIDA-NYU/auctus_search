import re
from typing import Any, Callable, Dict
from typing import Optional
from typing import Union

import ipywidgets as widgets
from beartype import beartype
from millify import millify

from auctus_search.helpers import check_dict_keys


@beartype
class AuctusDatasetCard:
    @check_dict_keys("dataset_result", ("metadata", "id"))
    def __init__(
        self,
        dataset_result: Dict[str, Any],
        select_callback_function: Optional[Callable[[Any, str], None]] = None,
        style_overrides: Optional[Dict[str, Dict[str, str]]] = None,
    ) -> None:
        self.dataset_result: Dict[str, Any] = dataset_result
        self.select_callback_function: Optional[Callable[[Any, str], None]] = (
            select_callback_function
        )
        self.style_overrides: Dict[str, Dict[str, str]] = (
            style_overrides if style_overrides is not None else {}
        )

        self._extract_metadata()
        self._format_dataset_description()
        self.formatted_dataset_size: str = self._format_dataset_size(self.dataset_size)
        self._initialize_select_button()

    def _extract_metadata(self) -> None:
        if not isinstance(self.dataset_result, dict):
            raise ValueError("Invalid dataset result. Must be a dictionary.")
        if "metadata" not in self.dataset_result or "id" not in self.dataset_result:
            raise ValueError(
                "Invalid dataset result. Must contain 'metadata' and 'id' keys."
            )

        metadata: Dict[str, Any] = self.dataset_result["metadata"]
        self.dataset_name: str = metadata.get("name", "Unknown Name")
        self.dataset_identifier: Any = self.dataset_result["id"]
        self.dataset_description: str = metadata.get(
            "description", "No description available."
        )
        self.dataset_source_url: str = metadata.get("source", "#")
        dataset_types: list[str] = metadata.get("types", ["Unknown"])
        self.dataset_type: str = (
            "Spatial"
            if "spatial" in metadata.get("types", [])
            else (dataset_types[0].capitalize() if dataset_types else "Unknown")
        )
        self.dataset_relevancy_score: float = round(self.dataset_result["score"], 2)
        self.dataset_size: Union[int, str] = metadata.get("nb_rows", "N/A")

    def _format_dataset_description(self) -> None:
        self.cleaned_dataset_description: str = re.sub(
            r"[\"']", "", self.dataset_description
        )
        if len(self.cleaned_dataset_description) <= 250:
            self.truncated_dataset_description: str = self.cleaned_dataset_description
            self.dataset_description_tooltip: str = ""
        else:
            self.truncated_dataset_description = (
                self.cleaned_dataset_description[:250] + "..."
            )
            self.dataset_description_tooltip = self.cleaned_dataset_description

    def _format_dataset_size(self, dataset_size_value: Union[int, str]) -> str:
        try:
            dataset_size_integer: int = int(dataset_size_value)
        except (ValueError, TypeError):
            return "N/A"
        return millify(dataset_size_integer, precision=0)

    def _initialize_select_button(self) -> None:
        self.select_dataset_button: widgets.Button = widgets.Button(
            description="Select Data",
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
            self.select_callback_function(self.dataset_identifier, self.dataset_name)

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
            {"margin": "0", "font-size": "24px", "font-weight": "700", "color": "#333"},
        )
        return f'<h3 style="{title_style}">{self.dataset_name}</h3>'

    def _render_dataset_source_link(self) -> str:
        paragraph_style: str = self._get_component_style(
            "source_paragraph",
            {"font-size": "15px", "color": "#007aff", "margin": "5px 0"},
        )
        anchor_style: str = self._get_component_style(
            "source_anchor", {"text-decoration": "none", "color": "#007aff"}
        )
        return f'<p style="{paragraph_style}"><a href="{self.dataset_source_url}" target="_blank" style="{anchor_style}">{self.dataset_source_url}</a></p>'

    def _render_dataset_description(self) -> str:
        paragraph_style: str = self._get_component_style(
            "description",
            {
                "font-size": "12px",
                "color": "#666",
                "margin": "5px 0",
                "flex-grow": "1",
                "overflow": "hidden",
            },
        )
        extra_information: str = (
            f'<span style="color: blue; cursor: pointer;" title="{self.dataset_description_tooltip}">hover for more</span>'
            if self.dataset_description_tooltip
            else ""
        )
        return f'<p style="{paragraph_style}">{self.truncated_dataset_description} {extra_information}</p>'

    def _render_tag(self, tag_label: str, tag_value: str, tag_position: str) -> str:
        default_tag_styles: Dict[str, str] = {
            "border-radius": "50px",
            "background-color": "white",
            "box-shadow": "0px 2px 16px rgba(0, 0, 0, 0.15)",
            "width": "98px",
            "height": "33px",
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "justify-content": "center",
            "text-align": "center",
            "font-weight": "700",
        }
        tag_container_style: str = (
            f"position: absolute; {tag_position}; "
            + self._get_component_style("tag", default_tag_styles)
        )
        tag_label_style: str = self._get_component_style(
            "tag_label",
            {
                "font-size": "8px",
                "color": "rgba(0, 0, 0, 0.3)",
                "margin-bottom": "-15px",
            },
        )
        tag_value_style: str = self._get_component_style(
            "tag_value", {"font-size": "14px", "color": "#007AFF"}
        )
        return f'<div style="{tag_container_style}"><span style="{tag_label_style}">{tag_label}</span><span style="{tag_value_style}">{tag_value}</span></div>'

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
            },
        )
        gauge_dash_offset: float = 251 - (self.dataset_relevancy_score / 100) * 251
        return f'''
        <div style="{gauge_container_style}">
            <svg width="72" height="72" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="#EEE" stroke-width="10" fill="none"/>
                <circle cx="50" cy="50" r="40" stroke="#007AFF" stroke-width="10" fill="none"
                    stroke-dasharray="251" stroke-dashoffset="{gauge_dash_offset}" transform="rotate(-90,50,50)"/>
                <text x="50" y="55" font-size="16" font-weight="bold" text-anchor="middle" fill="#007AFF">
                    {self.dataset_relevancy_score}%
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
            },
        )
        return f'<p style="{relevancy_label_style}">Relevancy</p>'

    def render(self) -> widgets.VBox:
        card_style: str = self._get_component_style(
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
                "justify-content": "space-between",
                "font-family": "'SF Pro', Arial, sans-serif",
                "position": "relative",
            },
        )
        card_html: str = f'''
        <div style="{card_style}">
            {self._render_dataset_title()}
            {self._render_dataset_source_link()}
            {self._render_dataset_description()}
            {self._render_tag("Type", self.dataset_type, "bottom: 20px; left: 15px")}
            {self._render_tag("Size", self.formatted_dataset_size, "bottom: 20px; right: 15px")}
            {self._render_relevancy_gauge()}
            {self._render_relevancy_label()}
        </div>
        '''
        card_widget: widgets.HTML = widgets.HTML(value=card_html)
        return widgets.VBox([card_widget, self.select_dataset_button])
