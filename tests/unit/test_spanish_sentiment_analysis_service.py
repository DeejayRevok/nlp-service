from unittest import TestCase

from spacy.cli import download

from services.nlp.spanish_nlp_service import SpanishNLPService
from services.sentiment_analysis.spanish_sentiment_analysis_service import SpanishSentimentAnalysisService


class TestSpanishSentimentAnalysisService(TestCase):

    TEST_NEGATIVE_SENTENCES = ["Esta frase es algo buena", "Esta frase es mala", "Esta frase es muy negativa"]
    TEST_POSITIVE_SENTENCES = ["Esta frase es algo mala", "Esta frase es buena", "Esta frase es muy buena"]
    TEST_POSITIVE_NEGATED_SENTENCE = ["Esta frase no es buena"]
    TEST_NEGATIVE_NEGATED_SENTENCE = ["Esta frase no es mala"]

    @classmethod
    def setUpClass(cls) -> None:
        download("es_core_news_md")

    def setUp(self) -> None:
        self.nlp_service = SpanishNLPService()
        self.sentiment_analysis_service = SpanishSentimentAnalysisService(self.nlp_service)

    def test_negative_sentiment(self):
        sentiment_score = self.sentiment_analysis_service.analyze(self.TEST_NEGATIVE_SENTENCES)

        self.assertLess(sentiment_score, 0)

    def test_positive_sentiment(self):
        sentiment_score = self.sentiment_analysis_service.analyze(self.TEST_POSITIVE_SENTENCES)

        self.assertGreater(sentiment_score, 0)

    def test_positive_negated_sentiment(self):
        sentiment_score = self.sentiment_analysis_service.analyze(self.TEST_POSITIVE_NEGATED_SENTENCE)
        self.assertLess(sentiment_score, 0)

    def test_negative_negated_sentiment(self):
        sentiment_score = self.sentiment_analysis_service.analyze(self.TEST_NEGATIVE_NEGATED_SENTENCE)
        self.assertGreater(sentiment_score, 0)
