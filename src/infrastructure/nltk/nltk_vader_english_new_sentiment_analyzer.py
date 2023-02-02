from nltk.sentiment import SentimentIntensityAnalyzer

from domain.new.language import Language
from domain.new.new import New
from domain.new.new_sentiment_analyzer import NewSentimentAnalyzer
from infrastructure.spacy.spacy_text_processor_factory import SpacyTextProcessorFactory


class NLTKVADEREnglishNewSentimentAnalyzer(NewSentimentAnalyzer):
    def __init__(self, spacy_text_processor_factory: SpacyTextProcessorFactory):
        self.__spacy_text_processor_factory = spacy_text_processor_factory
        self.__sentiment_intensity_analyzer = SentimentIntensityAnalyzer()

    def analyze(self, new: New) -> float:
        spacy_text_processor = self.__spacy_text_processor_factory.get_processor(Language.ENGLISH)

        content_doc = spacy_text_processor.process(new.content)

        sentence_scores = []
        for sentence in content_doc.sents:
            sentence = str(sentence)
            sentence_score = self.__sentiment_intensity_analyzer.polarity_scores(sentence)
            sentence_scores.append(sentence_score["compound"])

        return sum(sentence_scores) / len(sentence_scores)
