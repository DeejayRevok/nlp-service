from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.nltk.nltk_vader_english_new_sentiment_analyzer.NLTKVADEREnglishNewSentimentAnalyzer",
            "infrastructure.nltk.nltk_vader_english_new_sentiment_analyzer.NLTKVADEREnglishNewSentimentAnalyzer",
            [Argument.no_kw_argument("@infrastructure.spacy.spacy_text_processor_factory.SpacyTextProcessorFactory")],
        )
    )
