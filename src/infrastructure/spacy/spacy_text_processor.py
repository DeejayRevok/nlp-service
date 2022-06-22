from spacy import load
from spacy.tokens import Doc


class SpacyTextProcessor:
    def __init__(self, spacy_language_model_name: str):
        self.__spacy_language_model = load(spacy_language_model_name)

    def process(self, text: str) -> Doc:
        return self.__spacy_language_model(text)
