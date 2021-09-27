from math import sqrt
from os.path import join

from spacy.tokens import Span, Token
from typing import Union, List, Iterator

from config import RESOURCES_PATH
from log_config import get_logger
from services.nlp.nlp_service import NLPService
from services.sentiment_analysis.sentiment_analysis_service import SentimentAnalysisService

LOGGER = get_logger()


class SpanishSentimentAnalysisService(SentimentAnalysisService):
    def __init__(self, nlp_service: NLPService):
        self.__nlp_service = nlp_service
        with open(join(RESOURCES_PATH, "sentiment_lexicon/booster_increase.txt"), "r") as file:
            self.__boosters_increase = list(map(lambda word: word.strip(), file.readlines()))

        with open(join(RESOURCES_PATH, "sentiment_lexicon/booster_decrease.txt"), "r") as file:
            self.__boosters_decrease = list(map(lambda word: word.strip(), file.readlines()))

        with open(join(RESOURCES_PATH, "sentiment_lexicon/negative_lexicon.txt"), "r") as file:
            self.__negatives = list(map(lambda word: word.strip(), file.readlines()))

        with open(join(RESOURCES_PATH, "sentiment_lexicon/positive_lexicon.txt"), "r") as file:
            self.__positives = list(map(lambda word: word.strip(), file.readlines()))

    def analyze(self, sentences: Union[List[str], List[Span]]) -> float:
        LOGGER.info("Starting sentiment analysis for %d sentences", len(sentences))
        sentiment = 0
        for sentence in sentences:
            sentiment += self.__get_sentence_sentiment(sentence)
        return sentiment

    def __get_sentence_sentiment(self, sentence: Union[str, Span]) -> float:
        sentence_sentiment = 0
        sentence = sentence if not isinstance(sentence, str) else self.__nlp_service.process_text(sentence)
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

    def __apply_token_boosters(self, sentiment: float, token_childrens: Iterator[Token]) -> float:
        for children in token_childrens:
            if children.pos_ == "ADV":
                if children.lemma_.lower() in self.__boosters_increase:
                    sentiment = 1.2 * sentiment
                elif children.lemma_.lower() in self.__boosters_decrease:
                    sentiment = 0.8 * sentiment
                elif children.lower_ == "no":
                    sentiment = -sentiment
        return sentiment
