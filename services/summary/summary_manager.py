from spacy.tokens import Span
from typing import Union, List

from services.summary.summary_service import SummaryService


class SummaryManager:
    def __init__(self, **summary_services: SummaryService):
        self.__summary_services = dict()
        for language, summary_service in summary_services.items():
            self.__summary_services[language] = summary_service

    def summarize(self, language: str, sentences: Union[List[str], List[Span]]) -> str:
        return self.__summary_services[language].summarize(sentences)
