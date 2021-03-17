"""
Sentiment analysis module
"""
from math import sqrt
from os.path import join
from typing import List, Iterator, Union

from spacy.cli import download
from spacy.tokens import Token, Span

from config import RESOURCES_PATH
from log_config import get_logger
from services.nlp_service import NlpService

LOGGER = get_logger()


def initialize_sentiment_analysis():
    """
    Initialize the sentiment analyzer downloading the required resources (Spacy spanish model)
    """
    LOGGER.info('Downloading spacy spanish model')
    download('es_core_news_md')


class SentimentAnalysisService:
    """
    Sentiment analyzer implementation
    """
    def __init__(self, nlp_service: NlpService):
        """
        Initialize the sentiment analyzer loading the required lexicons and loading the required nlp components
        """
        self._nlp_service = nlp_service
        with open(join(RESOURCES_PATH, 'sentiment_lexicon/booster_increase.txt'), 'r') as file:
            self._boosters_increase = list(map(lambda word: word.strip(), file.readlines()))

        with open(join(RESOURCES_PATH, 'sentiment_lexicon/booster_decrease.txt'), 'r') as file:
            self._boosters_decrease = list(map(lambda word: word.strip(), file.readlines()))

        with open(join(RESOURCES_PATH, 'sentiment_lexicon/negative_lexicon.txt'), 'r') as file:
            self._negatives = list(map(lambda word: word.strip(), file.readlines()))

        with open(join(RESOURCES_PATH, 'sentiment_lexicon/positive_lexicon.txt'), 'r') as file:
            self._positives = list(map(lambda word: word.strip(), file.readlines()))

    def __call__(self, sentences: Union[List[str], List[Span]]) -> float:
        """
        Analyze the sentiment of the given sentences list

        Args:
            sentences: list of sentences to analyze sentiment

        Returns: overall sentiment of the input sentences

        """
        LOGGER.info('Starting sentiment analysis for %d sentences', len(sentences))
        sentiment = 0
        for sentence in sentences:
            sentiment += self._get_sentence_sentiment(sentence)
        return sentiment

    def _get_sentence_sentiment(self, sentence: Union[str, Span]) -> float:
        """
        Get the sentiment score for the input sentence

        Args:
            sentence: sentence to compute sentiment

        Returns: sentiment of the sentence

        """
        sentence_sentiment = 0
        sentence = sentence if not isinstance(sentence, str) else self._nlp_service.process_text(sentence)
        for token in sentence:
            sentence_sentiment += self._get_token_sentiment(token)

        return sentence_sentiment/sqrt(sentence_sentiment*sentence_sentiment + 15)

    def _get_token_sentiment(self, token: Token) -> float:
        """
        Get the sentiment score for the input token

        Args:
            token: token to get sentiment

        Returns: sentiment of the token

        """
        if token.lemma_.lower() in self._negatives:
            return self._apply_token_boosters(-1, token.children)
        elif token.lemma_.lower() in self._positives:
            return self._apply_token_boosters(1, token.children)
        else:
            return 0

    def _apply_token_boosters(self, sentiment: float, token_childrens: Iterator[Token]) -> float:
        """
        Apply the sentiment boosters to the given token sentiment

        Args:
            sentiment: base token sentiment
            token_childrens: token childrens to look for boosters

        Returns: sentiment boosted

        """
        for children in token_childrens:
            if children.pos_ == 'ADV':
                if children.lemma_.lower() in self._boosters_increase:
                    sentiment = 1.2 * sentiment
                elif children.lemma_.lower() in self._boosters_decrease:
                    sentiment = 0.8 * sentiment
                elif children.lower_ == 'no':
                    sentiment = -sentiment
        return sentiment