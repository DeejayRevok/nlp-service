from typing import Optional

from domain.new.language import Language
from domain.new.language_not_supported_exception import LanguageNotSupportedException
from infrastructure.spacy.spacy_text_processor import SpacyTextProcessor


class SpacyTextProcessorFactory:
    __SPACY_SPANISH_MODEL_NAME = "es_core_news_md"
    __SPACY_ENGLISH_MODEL_NAME = "en_core_web_md"

    def __init__(self):
        self.__spacy_spanish_text_processor: Optional[SpacyTextProcessor] = None
        self.__spacy_english_text_processor: Optional[SpacyTextProcessor] = None

    def get_processor(self, language: Language) -> SpacyTextProcessor:
        if language == language.SPANISH:
            return self.__get_spanish_processor()
        if language == language.ENGLISH:
            return self.__get_english_processor()
        raise LanguageNotSupportedException(language)

    def __get_spanish_processor(self) -> SpacyTextProcessor:
        if self.__spacy_spanish_text_processor is not None:
            return self.__spacy_spanish_text_processor
        return SpacyTextProcessor(self.__SPACY_SPANISH_MODEL_NAME)

    def __get_english_processor(self) -> SpacyTextProcessor:
        if self.__spacy_english_text_processor is not None:
            return self.__spacy_english_text_processor
        return SpacyTextProcessor(self.__SPACY_ENGLISH_MODEL_NAME)
