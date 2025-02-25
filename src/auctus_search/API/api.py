from beartype import beartype


@beartype
class AuctusAPI:
    BASE_URL: str = "https://auctus.vida-nyu.org/api/v1"

    @classmethod
    @beartype
    def search(cls, page: int = 1, size: int = 10) -> str:
        return f"{cls.BASE_URL}/search?page={page}&size={size}"

    @classmethod
    @beartype
    def download(cls, dataset_id: str, dataset_format: str = "csv") -> str:
        return f"{cls.BASE_URL}/download/{dataset_id}?format={dataset_format}"
