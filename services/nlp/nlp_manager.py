from spacy.tokens import Doc

from services.nlp.nlp_service import NLPService


class NLPManager:
    def __init__(self, **nlp_services: NLPService):
        self.__nlp_services = dict()
        for language, sentiment_analysis_service in nlp_services.items():
            self.__nlp_services[language] = sentiment_analysis_service

    def process_text(self, language: str, text: str) -> Doc:
        return self.__nlp_services[language].process_text(text)

    def doc_from_json_dict(self, language: str, doc_dict: dict) -> Doc:
        return self.__nlp_services[language].doc_from_json_dict(doc_dict)

    def doc_to_json_dict(self, language: str, doc: Doc) -> dict:
        return self.__nlp_services[language].doc_to_json_dict(doc)
