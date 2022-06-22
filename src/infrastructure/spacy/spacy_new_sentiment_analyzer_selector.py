from domain.new.language import Language
from domain.new.language_not_supported_exception import LanguageNotSupportedException
from domain.new.new_sentiment_analyzer import NewSentimentAnalyzer
from domain.new.new_sentiment_analyzer_selector import NewSentimentAnalyzerSelector
from infrastructure.nltk.nltk_vader_english_new_sentiment_analyzer import NLTKVADEREnglishNewSentimentAnalyzer
from infrastructure.spacy.spacy_spanish_new_sentiment_analyzer import SpacySpanishNewSentimentAnalyzer


class SpacyNewSentimentAnalyzerSelector(NewSentimentAnalyzerSelector):
    def __init__(
            self,
            spanish_sentiment_analyzer: SpacySpanishNewSentimentAnalyzer,
            english_sentiment_analyzer: NLTKVADEREnglishNewSentimentAnalyzer
    ):
        self.__spanish_sentiment_analyzer = spanish_sentiment_analyzer
        self.__english_sentiment_analyzer = english_sentiment_analyzer

    def select(self, language: Language) -> NewSentimentAnalyzer:
        if language == Language.SPANISH:
            return self.__spanish_sentiment_analyzer
        if language == Language.ENGLISH:
            return self.__english_sentiment_analyzer
        raise LanguageNotSupportedException(language)
