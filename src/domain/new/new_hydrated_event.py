from dataclasses import dataclass
from typing import List, Optional

from domain.named_entity.named_entity import NamedEntity


@dataclass(frozen=True)
class NewHydratedEvent:
    title: str
    url: str
    content: str
    source: str
    date: float
    language: str
    hydrated: bool
    entities: List[NamedEntity]
    summary: Optional[str] = None
    sentiment: Optional[float] = None
    image: Optional[str] = None
