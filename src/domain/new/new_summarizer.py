from abc import abstractmethod
from typing import Protocol

from domain.new.new import New


class NewSummarizer(Protocol):
    @abstractmethod
    def summarize(self, new: New) -> str:
        pass
