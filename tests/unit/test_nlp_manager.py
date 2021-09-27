from unittest import TestCase

from spacy.tokens import Doc
from unittest.mock import Mock

from services.nlp.nlp_manager import NLPManager
from services.nlp.nlp_service import NLPService


class TestNLPManager(TestCase):
    def setUp(self) -> None:
        self.language1 = "language1"
        self.language2 = "language2"
        self.nlp_service1_mock = Mock(spec=NLPService)
        self.nlp_service2_mock = Mock(spec=NLPService)
        self.nlp_manager = NLPManager(**{"language1": self.nlp_service1_mock, "language2": self.nlp_service2_mock})

    def test_process_text(self):
        test_text = "test_text"
        test_doc = Mock(spec=Doc)
        self.nlp_service1_mock.process_text.return_value = test_doc

        processed_doc = self.nlp_manager.process_text(self.language1, test_text)

        self.assertEqual(test_doc, processed_doc)
        self.nlp_service1_mock.process_text.assert_called_once_with(test_text)
        self.nlp_service2_mock.process_text.assert_not_called()

    def test_doc_from_json_dict(self):
        test_json = {"test": "Test"}
        test_doc = Mock(spec=Doc)
        self.nlp_service2_mock.doc_from_json_dict.return_value = test_doc

        transformed_doc = self.nlp_manager.doc_from_json_dict(self.language2, test_json)

        self.assertEqual(test_doc, transformed_doc)
        self.nlp_service2_mock.doc_from_json_dict.assert_called_once_with(test_json)
        self.nlp_service1_mock.doc_from_json_dict.assert_not_called()

    def test_doc_to_json_dict(self):
        test_json = {"test": "Test"}
        test_doc = Mock(spec=Doc)
        self.nlp_service2_mock.doc_to_json_dict.return_value = test_json

        doc_dict = self.nlp_manager.doc_to_json_dict(self.language2, test_doc)

        self.assertEqual(test_json, doc_dict)
        self.nlp_service2_mock.doc_to_json_dict.assert_called_once_with(test_doc)
        self.nlp_service1_mock.doc_to_json_dict.assert_not_called()
