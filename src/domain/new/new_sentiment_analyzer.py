from abc import abstractmethod
from typing import Protocol

from domain.new.new import New


class NewSentimentAnalyzer(Protocol):
    @abstractmethod
    def analyze(self, new: New) -> float:
        pass
