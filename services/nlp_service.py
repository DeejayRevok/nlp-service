"""
NLP functions module
"""
import base64
import numpy as np

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

    def doc_from_json_dict(self, doc_dict: dict) -> Doc:
        """
        Transform a jsonable dictionary into a NLP document

        Args:
            doc_dict: dictionary representation of a NLP document

        Returns: NLP document with the dictionary representation

        """
        new_doc_dict = doc_dict.copy()
        new_doc_dict['array_body'] = np.array(new_doc_dict['array_body'], dtype=np.uint64)
        new_doc_dict['tensor'] = np.array(new_doc_dict['tensor'])
        new_doc_dict['spans'] = base64.b64decode(new_doc_dict['spans'].encode('UTF-8'))
        return Doc(self.nlp_vocab()).from_dict(new_doc_dict)

    @staticmethod
    def doc_to_json_dict(doc: Doc) -> dict:
        """
        Transform a NLP document to a jsonable dictionary

        Args:
            doc: NLP document

        Returns: jsonable dictionary representation of the input doc

        """
        doc_dict = doc.to_dict()
        doc_dict['array_body'] = doc_dict['array_body'].tolist()
        doc_dict['tensor'] = doc_dict['tensor'].tolist()
        doc_dict['spans'] = base64.b64encode(doc_dict['spans']).decode('UTF-8')
        return doc_dict
