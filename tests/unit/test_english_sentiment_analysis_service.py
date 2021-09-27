from unittest import TestCase

from nltk import download

from services.sentiment_analysis.english_sentiment_analysis_service import EnglishSentimentAnalysisService


class TestEnglishSentimentAnalysisService(TestCase):

    TEST_NEGATIVE_SENTENCES = ["This sentence is a bit good", "This sentence is bad", "This sentence is so bad"]
    TEST_POSITIVE_SENTENCES = ["This sentence is a bit bad", "This sentence is good", "This sentence is so good"]
    TEST_POSITIVE_NEGATED_SENTENCE = ["This sentence is not good"]
    TEST_NEGATIVE_NEGATED_SENTENCE = ["This sentence is not bad"]

    @classmethod
    def setUpClass(cls) -> None:
        download("vader_lexicon")

    def setUp(self) -> None:
        self.english_sentiment_analysis_service = EnglishSentimentAnalysisService()

    def test_negative_sentiment(self):
        sentiment_score = self.english_sentiment_analysis_service.analyze(self.TEST_NEGATIVE_SENTENCES)

        self.assertLess(sentiment_score, 0)

    def test_positive_sentiment(self):
        sentiment_score = self.english_sentiment_analysis_service.analyze(self.TEST_POSITIVE_SENTENCES)

        self.assertGreater(sentiment_score, 0)

    def test_positive_negated_sentiment(self):
        sentiment_score = self.english_sentiment_analysis_service.analyze(self.TEST_POSITIVE_NEGATED_SENTENCE)

        self.assertLess(sentiment_score, 0)

    def test_negative_negated_sentiment(self):
        sentiment_score = self.english_sentiment_analysis_service.analyze(self.TEST_NEGATIVE_NEGATED_SENTENCE)

        self.assertGreater(sentiment_score, 0)
