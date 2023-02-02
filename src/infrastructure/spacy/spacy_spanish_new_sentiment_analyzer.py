from math import sqrt
from os.path import join, dirname
from typing import Iterable

from spacy.tokens import Span, Token

from domain.new.language import Language
from domain.new.new import New
from domain.new.new_sentiment_analyzer import NewSentimentAnalyzer
from infrastructure.spacy.spacy_text_processor_factory import SpacyTextProcessorFactory


class SpacySpanishNewSentimentAnalyzer(NewSentimentAnalyzer):
    __RESOURCES_PATH = join(dirname(__file__), "resources", "spanish_sentiment_analysis")

    def __init__(self, spacy_text_processor_factory: SpacyTextProcessorFactory):
        self.__spacy_text_processor_factory = spacy_text_processor_factory
        with open(join(self.__RESOURCES_PATH, "booster_increase.txt"), "r") as file:
            self.__boosters_increase = list(map(lambda word: word.strip(), file.readlines()))

        with open(join(self.__RESOURCES_PATH, "booster_decrease.txt"), "r") as file:
            self.__boosters_decrease = list(map(lambda word: word.strip(), file.readlines()))

        with open(join(self.__RESOURCES_PATH, "negative_lexicon.txt"), "r") as file:
            self.__negatives = list(map(lambda word: word.strip(), file.readlines()))

        with open(join(self.__RESOURCES_PATH, "positive_lexicon.txt"), "r") as file:
            self.__positives = list(map(lambda word: word.strip(), file.readlines()))

    def analyze(self, new: New) -> float:
        spacy_text_processor = self.__spacy_text_processor_factory.get_processor(Language.SPANISH)

        content_doc = spacy_text_processor.process(new.content)

        sentiment = 0
        for sentence in content_doc.sents:
            sentiment += self.__get_sentence_sentiment(sentence)
        return sentiment

    def __get_sentence_sentiment(self, sentence: Span) -> float:
        sentence_sentiment = 0
        for token in sentence:
            sentence_sentiment += self.__get_token_sentiment(token)

        return sentence_sentiment / sqrt(sentence_sentiment * sentence_sentiment + 15)

    def __get_token_sentiment(self, token: Token) -> float:
        if token.lemma_.lower() in self.__negatives:
            return self.__apply_token_boosters(-1, token.children)
        elif token.lemma_.lower() in self.__positives:
            return self.__apply_token_boosters(1, token.children)
        else:
            return 0

    def __apply_token_boosters(self, sentiment: float, token_childrens: Iterable[Token]) -> float:
        for children in token_childrens:
            if children.pos_ == "ADV":
                if children.lemma_.lower() in self.__boosters_increase:
                    sentiment = 1.2 * sentiment
                elif children.lemma_.lower() in self.__boosters_decrease:
                    sentiment = 0.8 * sentiment
                elif children.lower_ == "no":
                    sentiment = -sentiment
        return sentiment
