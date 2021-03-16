"""
Sentiment analyzer tests module
"""
from unittest import TestCase
from unittest.mock import patch

from services.nlp_service import NlpService
from services.sentiment_analysis_service import initialize_sentiment_analysis, SentimentAnalysisService


class TestSentimentAnalyzer(TestCase):

    TEST_NEGATIVE_SENTENCES = ['Esta frase es algo buena', 'Esta frase es mala', 'Esta frase es muy negativa']
    TEST_POSITIVE_SENTENCES = ['Esta frase es algo mala', 'Esta frase es buena', 'Esta frase es muy buena']
    TEST_POSITIVE_NEGATED_SENTENCE = ['Esta frase no es buena']
    TEST_NEGATIVE_NEGATED_SENTENCE = ['Esta frase no es mala']

    @patch('services.sentiment_analysis_service.download')
    def test_initialize_sentiment_analyzer(self, download_mock):
        """
        Test initialize sentiment analyzer downloads the required resources
        """
        initialize_sentiment_analysis()
        download_mock.assert_called_with('es_core_news_md')

    def test_negative_sentiment(self):
        """
        Test the sentiment analyzer with overall negative sentences returns negative score
        """
        initialize_sentiment_analysis()
        nlp_service = NlpService()
        sentiment_analyzer = SentimentAnalysisService(nlp_service)
        sentiment_score = sentiment_analyzer(self.TEST_NEGATIVE_SENTENCES)
        self.assertLess(sentiment_score, 0)

    def test_positive_sentiment(self):
        """
        Test the sentiment analyzer with overall positive sentences returns positive score
        """
        initialize_sentiment_analysis()
        nlp_service = NlpService()
        sentiment_analyzer = SentimentAnalysisService(nlp_service)
        sentiment_score = sentiment_analyzer(self.TEST_POSITIVE_SENTENCES)
        self.assertGreater(sentiment_score, 0)

    def test_positive_negated_sentiment(self):
        """
        Test the sentiment analyzer with positive negated sentence returns negative score
        """
        initialize_sentiment_analysis()
        nlp_service = NlpService()
        sentiment_analyzer = SentimentAnalysisService(nlp_service)
        sentiment_score = sentiment_analyzer(self.TEST_POSITIVE_NEGATED_SENTENCE)
        self.assertLess(sentiment_score, 0)

    def test_negative_negated_sentiment(self):
        """
        Test the sentiment analyzer with negative negated sentence returns positive score
        """
        initialize_sentiment_analysis()
        nlp_service = NlpService()
        sentiment_analyzer = SentimentAnalysisService(nlp_service)
        sentiment_score = sentiment_analyzer(self.TEST_NEGATIVE_NEGATED_SENTENCE)
        self.assertGreater(sentiment_score, 0)



