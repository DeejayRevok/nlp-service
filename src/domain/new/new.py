from dataclasses import dataclass, field
from typing import List, Optional

from domain.named_entity.named_entity import NamedEntity
from domain.new.language import Language


@dataclass
class New:
    title: str
    url: str
    content: str
    source: str
    date: float
    language: Language
    hydrated: bool = False
    entities: List[NamedEntity] = field(default_factory=list)
    summary: Optional[str] = None
    sentiment: Optional[float] = None
    image: Optional[str] = None
