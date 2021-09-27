from nltk.sentiment import SentimentIntensityAnalyzer
from spacy.tokens import Span
from typing import List, Union

from log_config import get_logger
from services.sentiment_analysis.sentiment_analysis_service import SentimentAnalysisService

LOGGER = get_logger()


class EnglishSentimentAnalysisService(SentimentAnalysisService):
    def analyze(self, sentences: Union[List[str], List[Span]]) -> float:
        LOGGER.info("Starting sentiment analysis for %d sentences", len(sentences))
        sid = SentimentIntensityAnalyzer()
        sentence_scores = []
        for sentence in sentences:
            if isinstance(sentence, Span):
                sentence = str(sentence)

            sentence_score = sid.polarity_scores(sentence)
            sentence_scores.append(sentence_score["compound"])

        return sum(sentence_scores) / len(sentence_scores)
