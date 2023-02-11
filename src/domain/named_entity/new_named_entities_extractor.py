from abc import abstractmethod
from typing import Protocol, Iterable

from domain.named_entity.named_entity import NamedEntity
from domain.new.new import New


class NewNamedEntitiesExtractor(Protocol):
    @abstractmethod
    def extract(self, new: New) -> Iterable[NamedEntity]:
        pass
