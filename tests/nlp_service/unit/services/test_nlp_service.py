"""
NLP service tests module
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from aiounittest import async_test
from news_service_lib.models import New

from services.nlp_service import NlpService


class TestNlpService(TestCase):
    """
    NLP service test cases implementation
    """
    TEST_NEW = New(title='test_title', url='https://test.test', content='test_content', date=2124124.0,
                   source='test_source')
    TEST_TEXT = 'test_text'
    TEST_ENTITY = ('test_entity_text', 'test_entity_type')
    TEST_SENTENCES = ['test_sentence_1', 'test_sentence_2']

    @patch('services.nlp_service.spacy')
    @async_test
    async def test_process_text(self, mocked_spacy):
        """
        Test process text returns the NLP processed doc with the sentences and the named entities extracted from
        the text
        """
        nlp_mock = MagicMock()
        mock_first_sentence = MagicMock()
        mock_first_sentence.__str__.return_value = self.TEST_SENTENCES[0]
        mock_second_sentence = MagicMock()
        mock_second_sentence.__str__.return_value = self.TEST_SENTENCES[1]

        mock_entity = MagicMock()
        mock_entity.__str__.return_value = self.TEST_ENTITY[0]
        mock_entity.label_ = self.TEST_ENTITY[1]

        doc_mock = MagicMock()
        nlp_mock.configure_mock(name='doc_mock')
        doc_mock.sents = [mock_first_sentence, mock_second_sentence]
        doc_mock.ents = [mock_entity]

        nlp_mock.configure_mock(name='nlp_mock')
        nlp_mock.return_value = doc_mock
        mocked_spacy.load.return_value = nlp_mock

        nlp_service = NlpService()
        nlp_doc = await nlp_service.get_processed_text(self.TEST_TEXT)
        nlp_mock.assert_called_with(self.TEST_TEXT)
        self.assertListEqual(nlp_doc.named_entities, [self.TEST_ENTITY])
        self.assertListEqual(nlp_doc.sentences, self.TEST_SENTENCES)

    @patch('services.nlp_service.publish_hydrated_new')
    @patch('services.nlp_service.hydrate_new_with_entities')
    @patch('services.nlp_service.spacy')
    @async_test
    async def test_hydrate_new(self, _, mocked_hydrate_new_entities, __):
        """
        Test hydrate new builds a chain linking all the specified tasks one behind another and calls the chain
        """
        hydrate_task_mock = MagicMock()
        NlpService.CELERY_NLP_PIPELINE = [mocked_hydrate_new_entities, hydrate_task_mock]
        mock_chain = MagicMock()
        mocked_hydrate_new_entities.s.return_value = mock_chain
        nlp_service = NlpService()
        await nlp_service.hydrate_new(dict(self.TEST_NEW))
        nlp_service.CELERY_NLP_PIPELINE[0].s.assert_called_with(dict(self.TEST_NEW))
        for task_mock in nlp_service.CELERY_NLP_PIPELINE[1:]:
            task_mock.s().link.assert_called_once()
        mock_chain.link.assert_called_with(hydrate_task_mock.s())
        mock_chain.delay.assert_called_once()
