from typing import Iterable

from spacy.tokens import Doc

from domain.named_entity.named_entity import NamedEntity
from domain.named_entity.new_named_entities_extractor import NewNamedEntitiesExtractor
from domain.new.new import New
from infrastructure.spacy.spacy_text_processor_factory import SpacyTextProcessorFactory


class SpacyNewNamedEntitiesExtractor(NewNamedEntitiesExtractor):
    def __init__(self, spacy_text_processor_factory: SpacyTextProcessorFactory):
        self.__spacy_text_processor_factory = spacy_text_processor_factory

    def extract(self, new: New) -> Iterable[NamedEntity]:
        spacy_text_processor = self.__spacy_text_processor_factory.get_processor(new.language)

        content_doc = spacy_text_processor.process(new.content)

        return self.__get_named_entities(content_doc)

    def __get_named_entities(self, spacy_doc: Doc) -> Iterable[NamedEntity]:
        for entity in spacy_doc.ents:
            yield NamedEntity(text=str(entity), type=entity.label_)
