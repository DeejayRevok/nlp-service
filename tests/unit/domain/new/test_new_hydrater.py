from unittest import TestCase
from unittest.mock import Mock

from domain.new.new_sentiment_analyzer import NewSentimentAnalyzer
from domain.named_entity.named_entity import NamedEntity
from domain.new.language import Language
from domain.new.new import New
from domain.new.new_sentiment_analyzer_selector import NewSentimentAnalyzerSelector
from domain.new.new_summarizer import NewSummarizer
from domain.named_entity.new_named_entities_extractor import NewNamedEntitiesExtractor
from domain.new.new_hydrater import NewHydrater


class TestNewHydrater(TestCase):
    def setUp(self) -> None:
        self.new_named_entities_extractor_mock = Mock(spec=NewNamedEntitiesExtractor)
        self.new_summarizer_mock = Mock(spec=NewSummarizer)
        self.new_sentiment_analyzer_selector_mock = Mock(spec=NewSentimentAnalyzerSelector)
        self.new_hydrater = NewHydrater(
            self.new_named_entities_extractor_mock, self.new_summarizer_mock, self.new_sentiment_analyzer_selector_mock
        )

    def test_hydrate_success(self):
        test_new = New(
            title="test_title",
            url="test_url",
            content="test_content",
            source="test_source",
            date=42432.89,
            language=Language.ENGLISH,
            image="test_image",
            hydrated=False,
        )
        test_named_entity = NamedEntity(text="test_named_entity", type="test_named_entity_type")
        self.new_named_entities_extractor_mock.extract.return_value = [test_named_entity, test_named_entity]
        test_sentiment_analyzer = Mock(spec=NewSentimentAnalyzer)
        test_sentiment_analyzer.analyze.return_value = 12.34
        self.new_sentiment_analyzer_selector_mock.select.return_value = test_sentiment_analyzer
        self.new_summarizer_mock.summarize.return_value = "test_new_summary"

        self.new_hydrater.hydrate(test_new)

        self.assertEqual([test_named_entity, test_named_entity], test_new.entities)
        self.assertEqual(12.34, test_new.sentiment)
        self.assertEqual("test_new_summary", test_new.summary)
        self.assertTrue(test_new.hydrated)
        self.new_named_entities_extractor_mock.extract.assert_called_once_with(test_new)
        self.new_sentiment_analyzer_selector_mock.select.assert_called_once_with(Language.ENGLISH)
        test_sentiment_analyzer.analyze.assert_called_once_with(test_new)
        self.new_summarizer_mock.summarize.assert_called_once_with(test_new)
