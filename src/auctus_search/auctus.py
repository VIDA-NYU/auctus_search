from beartype import beartype
from .mixins import AuctusSearchMixin, AuctusSearchLoaderMixin, AuctusSearchDisplayMixin


@beartype
class AuctusSearch(
    AuctusSearchMixin, AuctusSearchLoaderMixin, AuctusSearchDisplayMixin
):
    def __init__(self) -> None:
        super().__init__()
