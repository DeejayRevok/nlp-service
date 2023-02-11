from domain.named_entity.new_named_entities_extractor import NewNamedEntitiesExtractor
from domain.new.new import New
from domain.new.new_sentiment_analyzer_selector import NewSentimentAnalyzerSelector
from domain.new.new_summarizer import NewSummarizer


class NewHydrater:
    def __init__(
        self,
        new_named_entities_extractor: NewNamedEntitiesExtractor,
        new_summarizer: NewSummarizer,
        new_sentiment_analyzer_selector: NewSentimentAnalyzerSelector,
    ):
        self.__new_named_entities_extractor = new_named_entities_extractor
        self.__new_summarizer = new_summarizer
        self.__new_sentiment_analyzer_selector = new_sentiment_analyzer_selector

    def hydrate(self, new: New) -> None:
        new.entities = list(self.__new_named_entities_extractor.extract(new))

        new.summary = self.__new_summarizer.summarize(new)

        sentiment_analyzer = self.__new_sentiment_analyzer_selector.select(new.language)
        new.sentiment = sentiment_analyzer.analyze(new)

        new.hydrated = True
