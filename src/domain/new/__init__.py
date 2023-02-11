from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "domain.new.new_hydrater.NewHydrater",
            "domain.new.new_hydrater.NewHydrater",
            [
                Argument.no_kw_argument(
                    "@infrastructure.spacy.spacy_new_named_entities_extractor.SpacyNewNamedEntitiesExtractor"
                ),
                Argument.no_kw_argument("@infrastructure.spacy.spacy_new_summarizer.SpacyNewSummarizer"),
                Argument.no_kw_argument(
                    "@infrastructure.spacy.spacy_new_sentiment_analyzer_selector.SpacyNewSentimentAnalyzerSelector"
                ),
            ],
        )
    )
