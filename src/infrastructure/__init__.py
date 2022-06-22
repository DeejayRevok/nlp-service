from infrastructure.spacy import load as load_spacy
from infrastructure.nltk import load as load_nltk


def load() -> None:
    load_nltk()
    load_spacy()
