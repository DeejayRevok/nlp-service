"""
NLP functions module
"""
import spacy
from spacy.vocab import Vocab
from spacy.tokens import Doc


class NlpService:
    """
    NLP service implementation
    """

    def __init__(self):
        """
        Initialize the NLP service loading the language model
        """
        self._spanish_language = spacy.load('es_core_news_md')

    def process_text(self, text: str) -> Doc:
        """
        Process a text with the NLP language model

        Args:
            text: text to process

        Returns: processed text with NLP information

        """
        return self._spanish_language(text)

    def nlp_vocab(self) -> Vocab:
        """
        Get the NLP model vocabulary

        Returns: NLP model vocabulary

        """
        return self._spanish_language.vocab
