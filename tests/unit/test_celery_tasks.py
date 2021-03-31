"""
Celery tasks unit tests module
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from dynaconf.loaders import settings_loader
from pypendency.builder import container_builder
from spacy.cli import download
from news_service_lib.models import New, NamedEntity, NLPDoc

from config import config
from tests import TEST_CONFIG_PATH
from worker.celery_tasks import initialize_worker, process_new_content, hydrate_new, summarize, publish_hydrated_new, \
    sentiment_analysis


class TestNamedEntity:
    """
    Fake named entity used for testing
    """

    def __init__(self, text, type_value):
        self.text = text
        self.label_ = type_value

    def __str__(self):
        return self.text


class TestCeleryTasks(TestCase):
    """
    Celery tasks test cases implementation
    """
    TEST_NEW = New(title='test_title', url='https://test.test', content='test_content', source='test_source',
                   date=123123.0)
    TEST_ENTITIES = [NamedEntity(text='Test_ENTITY_text', type='test_entity_type')]
    TEST_NAMED_ENTITIES = [('Test_ENTITY_text', 'test_entity_type'), ('Test_ENTITY_text', 'test_entity_type')]
    TEST_PROCESSED_TEXT = NLPDoc(sentences=['test_sentence_1', 'test_sentence_2'],
                                 named_entities=TEST_NAMED_ENTITIES,
                                 noun_chunks=['test_noun_chunk'])
    TEST_NOUN_CHUNKS = ['Test_noun_chunk1', 'Test_noun_chunk2']
    TEST_SUMMARY = 'Test summary'
    TEST_SENTIMENT = 0.4

    TEST_NLP_SERVICE_CONFIG = dict(protocol='test_protocol', host='test_host', port='0')
    TEST_QUEUE_CONFIG = dict(host='test_host', port='0', user='test_user', password='test_password')

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the tests environment
        """
        download('es_core_news_md')

        cls.nlp_service_mock = MagicMock()
        cls.summarizer_mock = MagicMock()
        cls.sentiment_analyzer_mock = MagicMock()
        cls.exchange_publisher_mock = MagicMock()

        container_builder.set('services.nlp_service.NlpService', cls.nlp_service_mock)
        container_builder.set('services.summary_service.SummaryService', cls.summarizer_mock)
        container_builder.set('services.sentiment_analysis_service.SentimentAnalysisService',
                              cls.sentiment_analyzer_mock)
        container_builder.set('news_service_lib.messaging.exchange_publisher', cls.exchange_publisher_mock)

    @patch('worker.celery_tasks.CELERY_APP')
    def test_initialize_worker(self, _):
        """
        Test initializing the worker initializes and stores in the global variables the required services
        """
        initialize_worker()

        self.exchange_publisher_mock.connect.assert_called_once()
        self.exchange_publisher_mock.initialize.assert_called_once()

    @patch('worker.celery_tasks.CELERY_APP')
    def test_process_text(self, _):
        """
        Test processing the text returns the dictionary representation of the doc object
        """
        self.nlp_service_mock.doc_to_json_dict.return_value = dict(self.TEST_PROCESSED_TEXT)

        nlp_doc = process_new_content(dict(self.TEST_NEW))
        self.assertEqual(nlp_doc, dict(self.TEST_PROCESSED_TEXT))

    @patch('worker.celery_tasks.CELERY_APP')
    def test_hydrate_new(self, _):
        """
        Test hydrating the new hydrates all provided parameters
        """
        spacy_doc_mock = MagicMock()
        spacy_doc_mock.ents = [TestNamedEntity('Test_ENTITY_text', 'test_entity_type')]
        spacy_doc_mock.noun_chunks = self.TEST_NOUN_CHUNKS
        self.nlp_service_mock.doc_from_json_dict.return_value = spacy_doc_mock

        new = hydrate_new(dict(self.TEST_NEW), dict(self.TEST_PROCESSED_TEXT), self.TEST_SUMMARY, self.TEST_SENTIMENT)
        self.assertListEqual(new['entities'], [dict(entity) for entity in self.TEST_ENTITIES])
        self.assertListEqual(new['noun_chunks'], self.TEST_NOUN_CHUNKS)
        self.assertEqual(new['summary'], self.TEST_SUMMARY)
        self.assertEqual(new['sentiment'], self.TEST_SENTIMENT)

    @patch('worker.celery_tasks.CELERY_APP')
    def test_summarize(self, _):
        """
        Test the summarize task calls the summarizer service with the doc sentences and returns the summary
        """
        self.summarizer_mock.return_value = self.TEST_SUMMARY

        test_sentences = ['Sentence number one', 'Sentence number two']
        spacy_doc_mock = MagicMock()
        spacy_doc_mock.sents = test_sentences
        spacy_doc_mock.noun_chunks = self.TEST_NOUN_CHUNKS
        self.nlp_service_mock.doc_from_json_dict.return_value = spacy_doc_mock

        summary = summarize(dict(self.TEST_PROCESSED_TEXT))
        self.assertEqual(summary, self.TEST_SUMMARY)
        self.summarizer_mock.assert_called_with(test_sentences)

    @patch('worker.celery_tasks.CELERY_APP')
    def test_sentiment_analysis(self, _):
        """
        Test the sentiment analysis task calls the sentiment analyzer with the doc sentences and returns the sentiment
        """
        self.sentiment_analyzer_mock.return_value = self.TEST_SENTIMENT

        test_sentences = ['Sentence number one', 'Sentence number two']
        spacy_doc_mock = MagicMock()
        spacy_doc_mock.sents = test_sentences
        spacy_doc_mock.noun_chunks = self.TEST_NOUN_CHUNKS
        self.nlp_service_mock.doc_from_json_dict.return_value = spacy_doc_mock

        sentiment = sentiment_analysis(dict(self.TEST_PROCESSED_TEXT))
        self.assertEqual(sentiment, self.TEST_SENTIMENT)
        self.sentiment_analyzer_mock.assert_called_with(test_sentences)

    @patch('worker.celery_tasks.CELERY_APP')
    def test_publish_new(self, _, ):
        """
        Test publishing new declares the exchange, publish the new, sets hydrated of new as true, closes the channel
        and closes the connection
        """
        settings_loader(config, filename=TEST_CONFIG_PATH)

        publish_hydrated_new(dict(self.TEST_NEW))

        expected_new = dict(self.TEST_NEW)
        expected_new['hydrated'] = True
        self.exchange_publisher_mock.assert_called_with(expected_new)
