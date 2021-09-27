import base64
import numpy as np
import spacy
from spacy.tokens import Doc


class NLPService:
    def __init__(self, language_model_name: str):
        self.__language_model = spacy.load(language_model_name)

    def process_text(self, text: str) -> Doc:
        return self.__language_model(text)

    def doc_from_json_dict(self, doc_dict: dict) -> Doc:
        new_doc_dict = doc_dict.copy()
        new_doc_dict["array_body"] = np.array(new_doc_dict["array_body"], dtype=np.uint64)
        new_doc_dict["tensor"] = np.array(new_doc_dict["tensor"])
        new_doc_dict["spans"] = base64.b64decode(new_doc_dict["spans"].encode("UTF-8"))
        return Doc(self.__language_model.vocab).from_dict(new_doc_dict)

    def doc_to_json_dict(self, doc: Doc) -> dict:
        doc_dict = doc.to_dict()
        doc_dict["array_body"] = doc_dict["array_body"].tolist()
        doc_dict["tensor"] = doc_dict["tensor"].tolist()
        doc_dict["spans"] = base64.b64encode(doc_dict["spans"]).decode("UTF-8")
        return doc_dict
