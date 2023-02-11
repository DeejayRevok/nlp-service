from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.spacy.spacy_text_processor_factory.SpacyTextProcessorFactory",
            "infrastructure.spacy.spacy_text_processor_factory.SpacyTextProcessorFactory",
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.spacy.spacy_new_named_entities_extractor.SpacyNewNamedEntitiesExtractor",
            "infrastructure.spacy.spacy_new_named_entities_extractor.SpacyNewNamedEntitiesExtractor",
            [Argument.no_kw_argument("@infrastructure.spacy.spacy_text_processor_factory.SpacyTextProcessorFactory")],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.spacy.spacy_spanish_new_sentiment_analyzer.SpacySpanishNewSentimentAnalyzer",
            "infrastructure.spacy.spacy_spanish_new_sentiment_analyzer.SpacySpanishNewSentimentAnalyzer",
            [Argument.no_kw_argument("@infrastructure.spacy.spacy_text_processor_factory.SpacyTextProcessorFactory")],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.spacy.spacy_new_sentiment_analyzer_selector.SpacyNewSentimentAnalyzerSelector",
            "infrastructure.spacy.spacy_new_sentiment_analyzer_selector.SpacyNewSentimentAnalyzerSelector",
            [
                Argument.no_kw_argument(
                    "@infrastructure.spacy.spacy_spanish_new_sentiment_analyzer.SpacySpanishNewSentimentAnalyzer"
                ),
                Argument.no_kw_argument(
                    "@infrastructure.nltk"
                    ".nltk_vader_english_new_sentiment_analyzer.NLTKVADEREnglishNewSentimentAnalyzer"
                ),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.spacy.spacy_new_summarizer.SpacyNewSummarizer",
            "infrastructure.spacy.spacy_new_summarizer.SpacyNewSummarizer",
            [Argument.no_kw_argument("@infrastructure.spacy.spacy_text_processor_factory.SpacyTextProcessorFactory")],
        )
    )
