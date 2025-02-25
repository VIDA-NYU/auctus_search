from beartype import beartype
from DataProfileViewer import plot_data_summary

from auctus_search.helpers.ensure_dataset_identifier import ensure_dataset_identifier
from auctus_search.mixins.search import AuctusSearchMixin


@beartype
class DataProfileViewerMixin:
    @ensure_dataset_identifier
    @beartype
    def profile_selected_dataset(self: "AuctusSearchMixin") -> None:
        if not self.selected_dataset.metadata:
            raise ValueError("No metadata found. Please load a dataset first.")

        plot_data_summary(self.selected_dataset.metadata.to_dict())
