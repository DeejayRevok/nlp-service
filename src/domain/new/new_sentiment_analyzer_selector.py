from abc import abstractmethod
from typing import Protocol

from domain.new.language import Language
from domain.new.new_sentiment_analyzer import NewSentimentAnalyzer


class NewSentimentAnalyzerSelector(Protocol):
    @abstractmethod
    def select(self, language: Language) -> NewSentimentAnalyzer:
        pass
