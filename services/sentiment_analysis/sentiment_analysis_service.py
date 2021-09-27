from abc import abstractmethod
from nltk import download
from spacy.tokens import Span

from typing import List, Protocol, Union

from log_config import get_logger

LOGGER = get_logger()


def initialize_sentiment_analysis_service():
    LOGGER.info("Downloading sentiment analysis lexicon...")
    download('vader_lexicon')


class SentimentAnalysisService(Protocol):
    @abstractmethod
    def analyze(self, sentences: Union[List[str], List[Span]]) -> float:
        pass
