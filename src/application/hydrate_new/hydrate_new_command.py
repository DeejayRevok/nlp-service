from dataclasses import dataclass
from typing import Optional

from bus_station.command_terminal.command import Command


@dataclass(frozen=True)
class HydrateNewCommand(Command):
    title: str
    url: str
    content: str
    source: str
    date: float
    language: str
    image: Optional[str] = None

    @classmethod
    def passenger_name(cls) -> str:
        return "command.nlp_service.hydrate_new"
