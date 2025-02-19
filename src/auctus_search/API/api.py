from beartype import beartype


@beartype
class AuctusAPI:
    BASE_URL: str = "https://auctus.vida-nyu.org/api/v1"

    @classmethod
    def search(cls) -> str:
        return f"{cls.BASE_URL}/search"

    @classmethod
    def download(cls, dataset_id: str, dataset_format: str = "csv") -> str:
        return f"{cls.BASE_URL}/download/{dataset_id}?format={dataset_format}"
