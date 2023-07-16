from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class NewSavedEvent:
    title: str
    url: str
    content: str
    source: str
    date: float
    language: str
    hydrated: bool = False
    image: Optional[str] = None
