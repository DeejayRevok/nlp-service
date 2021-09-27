from spacy.tokens import Span
from typing import Union, List

from services.sentiment_analysis.sentiment_analysis_service import SentimentAnalysisService


class SentimentAnalysisManager:
    def __init__(self, **sentiment_analysis_services: SentimentAnalysisService):
        self.__sentiment_analysis_services = dict()
        for language, sentiment_analysis_service in sentiment_analysis_services.items():
            self.__sentiment_analysis_services[language] = sentiment_analysis_service

    def analyze(self, language: str, sentences: Union[List[str], List[Span]]) -> float:
        return self.__sentiment_analysis_services[language].analyze(sentences)
