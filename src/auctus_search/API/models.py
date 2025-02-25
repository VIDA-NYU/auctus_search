import dataclasses
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from beartype import beartype


@dataclass
@beartype
class Metadata:
    name: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    date: Optional[str] = None
    license: Optional[str] = None
    sample: Optional[str] = None
    types: List[str] = field(default_factory=list)
    size: Optional[int] = None
    nb_rows: Optional[int] = None
    nb_profiled_rows: Optional[int] = None
    version: Optional[str] = None
    columns: List[Dict[str, Any]] = field(default_factory=list)
    spatial_coverage: List[Dict[str, Any]] = field(default_factory=list)
    temporal_coverage: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclass
@beartype
class Dataset:
    id: str
    score: float
    metadata: Metadata
