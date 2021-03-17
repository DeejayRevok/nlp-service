"""
Celery tasks unit tests module
"""
import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

from dynaconf.loaders import settings_loader
from spacy.cli import download

from config import config
from news_service_lib.models import New, NamedEntity, NLPDoc

from services.nlp_service import NlpService
from tests import TEST_CONFIG_PATH
from worker import celery_tasks
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

    @patch('worker.celery_tasks.SummaryService')
    @patch('worker.celery_tasks.SentimentAnalysisService')
    @patch.object(NlpService, 'process_text')
    @patch('worker.celery_tasks.CELERY_APP')
    def test_initialize_worker(self, _, __, ___, ____):
        """
        Test initializing the worker initializes and stores in the global variables the required services
        """
        initialize_worker()

        from worker.celery_tasks import NLP_SERVICE
        self.assertIsNotNone(NLP_SERVICE)

        from worker.celery_tasks import SENTIMENT_ANALYZER
        self.assertIsNotNone(SENTIMENT_ANALYZER)

        from worker.celery_tasks import SUMMARIZER
        self.assertIsNotNone(SUMMARIZER)

    @patch.object(NlpService, 'doc_to_json_dict', return_value=dict(TEST_PROCESSED_TEXT))
    @patch.object(NlpService, 'process_text')
    @patch('worker.celery_tasks.CELERY_APP')
    def test_process_text(self, _, __, ___):
        """
        Test processing the text returns the dictionary representation of the doc object
        """
        initialize_worker()
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

        nlp_service_mock = MagicMock()
        nlp_service_mock.doc_from_json_dict.return_value = spacy_doc_mock
        celery_tasks.NLP_SERVICE = nlp_service_mock

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
        summarizer_mock = MagicMock()
        summarizer_mock.return_value = self.TEST_SUMMARY

        test_sentences = ['Sentence number one', 'Sentence number two']
        spacy_doc_mock = MagicMock()
        spacy_doc_mock.sents = test_sentences
        spacy_doc_mock.noun_chunks = self.TEST_NOUN_CHUNKS

        nlp_service_mock = MagicMock()
        nlp_service_mock.doc_from_json_dict.return_value = spacy_doc_mock
        celery_tasks.NLP_SERVICE = nlp_service_mock
        celery_tasks.SUMMARIZER = summarizer_mock
        summary = summarize(dict(self.TEST_PROCESSED_TEXT))
        self.assertEqual(summary, self.TEST_SUMMARY)
        summarizer_mock.assert_called_with(test_sentences)

    @patch('worker.celery_tasks.CELERY_APP')
    def test_sentiment_analysis(self, _):
        """
        Test the sentiment analysis task calls the sentiment analyzer with the doc sentences and returns the sentiment
        """
        sentiment_analyzer_mock = MagicMock()
        sentiment_analyzer_mock.return_value = self.TEST_SENTIMENT

        test_sentences = ['Sentence number one', 'Sentence number two']
        spacy_doc_mock = MagicMock()
        spacy_doc_mock.sents = test_sentences
        spacy_doc_mock.noun_chunks = self.TEST_NOUN_CHUNKS

        nlp_service_mock = MagicMock()
        nlp_service_mock.doc_from_json_dict.return_value = spacy_doc_mock
        celery_tasks.NLP_SERVICE = nlp_service_mock
        celery_tasks.SENTIMENT_ANALYZER = sentiment_analyzer_mock
        sentiment = sentiment_analysis(dict(self.TEST_PROCESSED_TEXT))
        self.assertEqual(sentiment, self.TEST_SENTIMENT)
        sentiment_analyzer_mock.assert_called_with(test_sentences)

    @patch('worker.celery_tasks.PlainCredentials')
    @patch('worker.celery_tasks.ConnectionParameters')
    @patch('worker.celery_tasks.BlockingConnection')
    @patch('worker.celery_tasks.CELERY_APP')
    def test_publish_new(self, _, mocked_connection, ___, ____):
        """
        Test publishing new declares the exchange, publish the new, sets hydrated of new as true, closes the channel
        and closes the connection
        """
        settings_loader(config, filename=TEST_CONFIG_PATH)

        initialize_worker()
        channel_mock = MagicMock()
        mocked_connection().channel.return_value = channel_mock
        publish_hydrated_new(dict(self.TEST_NEW))

        channel_mock.exchange_declare.assert_called_with(exchange='news-internal-exchange', exchange_type='fanout',
                                                         durable=True)
        self.TEST_NEW.hydrated = True
        channel_mock.basic_publish.assert_called_with(exchange='news-internal-exchange', routing_key='',
                                                      body=json.dumps(dict(self.TEST_NEW)))

        channel_mock.close.assert_called_once()
        mocked_connection().close.assert_called_once()
