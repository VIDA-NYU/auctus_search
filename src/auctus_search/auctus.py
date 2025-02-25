from beartype import beartype
from .mixins import (
    AuctusSearchMixin,
    AuctusSearchLoaderMixin,
    AuctusSearchDisplayMixin,
    DataProfileViewerMixin,
)


@beartype
class AuctusSearch(
    AuctusSearchMixin,
    AuctusSearchLoaderMixin,
    AuctusSearchDisplayMixin,
    DataProfileViewerMixin,
):
    def __init__(self) -> None:
        super().__init__()
