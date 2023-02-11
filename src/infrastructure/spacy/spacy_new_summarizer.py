from statistics import mean
from typing import Iterable, List, Tuple

from spacy.tokens import Span, Token
import numpy as np
import networkx as nx

from domain.new.new import New
from domain.new.new_summarizer import NewSummarizer
from infrastructure.spacy.spacy_text_processor_factory import SpacyTextProcessorFactory


class SpacyNewSummarizer(NewSummarizer):
    __SENTENCE_SIMILARITY_THRESHOLD = 0.8

    def __init__(self, spacy_text_processor_factory: SpacyTextProcessorFactory):
        self.__spacy_text_processor_factory = spacy_text_processor_factory

    def summarize(self, new: New) -> str:
        spacy_text_processor = self.__spacy_text_processor_factory.get_processor(new.language)

        content_doc = spacy_text_processor.process(new.content)
        content_sentences = list(content_doc.sents)

        sentences_similarity_matrix = self.__build_similarity_matrix(content_sentences)
        sentence_distance_graph = nx.from_numpy_array(sentences_similarity_matrix)
        sentence_scores = nx.pagerank(sentence_distance_graph)

        sentences_semantic_values = []
        for i, sentence in enumerate(content_sentences):
            sentence_semantic_value = self.__get_sentence_semantic_value(sentence)
            sentence_scores[i] = sentence_scores[i] * sentence_semantic_value
            sentences_semantic_values.append(sentence_semantic_value)

        summary_sentences_num = self.__get_summary_sentences_num(content_sentences)

        ranked_scores = {k: v for k, v in sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True)}
        ranked_sentences = list(ranked_scores.keys())
        qualifiers = ranked_sentences[:summary_sentences_num]
        non_qualifiers = ranked_sentences[summary_sentences_num:]

        self.__clean_qualifiers(qualifiers, non_qualifiers, sentences_similarity_matrix, sentences_semantic_values)

        summarize_text_sentences = []
        for i in sorted(qualifiers):
            sentence = str(content_sentences[i])
            summarize_text_sentences.append(sentence)

        return " ".join(summarize_text_sentences)

    def __get_sentence_semantic_value(self, sentence: Span) -> float:
        token_semantic_values = [
            self.__get_token_semantic_value(token) for token in self.__get_sentence_tokens(sentence)
        ]
        return mean(token_semantic_values)

    def __get_sentence_tokens(self, sentence: Span) -> Iterable[Token]:
        for token in sentence:
            if token.is_punct is False:
                yield token

    def __get_token_semantic_value(self, token: Token) -> int:
        return 1 if token.is_stop is False else 0

    def __build_similarity_matrix(self, sentences: Iterable[Span]) -> np.ndarray:
        sentences = list(sentences)
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for index_1, _ in enumerate(sentences):
            for index_2, _ in enumerate(sentences):
                if index_1 == index_2:
                    continue
                similarity_matrix[index_1][index_2] = self.__sentence_similarity(sentences[index_1], sentences[index_2])

        return similarity_matrix

    def __sentence_similarity(self, sentence_1: Span, sentence_2: Span) -> float:
        return sentence_1.similarity(sentence_2)

    def __get_summary_sentences_num(self, sentences: List[Span]) -> int:
        summary_sentences_num = round(len(sentences) / 4)
        summary_sentences_num = summary_sentences_num if summary_sentences_num >= 2 else 2
        summary_sentences_num = summary_sentences_num if summary_sentences_num <= 10 else 10
        return summary_sentences_num

    def __clean_qualifiers(
        self,
        qualifiers: List[int],
        non_qualifiers: List[int],
        sentences_similarity_matrix: np.ndarray,
        sentences_semantic_values: List[float],
    ):
        qualifiers_similarity_matrix = sentences_similarity_matrix[np.ix_(qualifiers, qualifiers)]
        similar_qualifiers_idxs = self.__get_most_similar_above_threshold(qualifiers_similarity_matrix)
        if len(non_qualifiers) > 0 and len(similar_qualifiers_idxs) > 0:
            new_qualifiers = []
            discarded_idxs = []
            qualifying_qualifier_idxs = []
            for idx1, idx2 in similar_qualifiers_idxs:
                if len(non_qualifiers) == 0:
                    break

                if (
                    idx1 in discarded_idxs
                    or idx2 in discarded_idxs
                    or idx1 in qualifying_qualifier_idxs
                    or idx2 in qualifying_qualifier_idxs
                ):
                    continue

                if sentences_semantic_values[qualifiers[idx1]] >= sentences_semantic_values[qualifiers[idx2]]:
                    discarded_idxs.append(idx2)
                    qualifying_qualifier_idxs.append(idx1)
                else:
                    discarded_idxs.append(idx1)
                    qualifying_qualifier_idxs.append(idx2)

                new_qualifiers.append(non_qualifiers.pop(0))

            qualifiers = self.__remove_discarded_qualifiers(qualifiers, discarded_idxs)
            qualifiers.extend(new_qualifiers)

            self.__clean_qualifiers(qualifiers, non_qualifiers, sentences_similarity_matrix, sentences_semantic_values)

    def __get_most_similar_above_threshold(self, qualifiers_similarity_matrix: np.ndarray) -> List[Tuple[int, int]]:
        max_similarities_idxs = []
        max_similarities = []
        for idx, similarities in enumerate(qualifiers_similarity_matrix):
            max_similarity_idx = np.argmax(similarities)
            max_similarity = similarities[max_similarity_idx]

            if max_similarity < self.__SENTENCE_SIMILARITY_THRESHOLD:
                continue

            if (max_similarity_idx, idx) in max_similarities_idxs:
                continue

            if len(max_similarities) > 0 and max_similarity > max_similarities[0]:
                max_similarities_idxs.insert(0, (idx, max_similarity_idx))
                max_similarities.insert(0, max_similarity)
                continue

            max_similarities_idxs.append((idx, max_similarity_idx))
            max_similarities.append(max_similarity)
        return max_similarities_idxs

    def __remove_discarded_qualifiers(self, qualifiers: List[int], discarded_idxs: List[int]) -> List[int]:
        cleaned_qualifiers = []
        for idx, qualifier in enumerate(qualifiers):
            if idx in discarded_idxs:
                continue
            cleaned_qualifiers.append(qualifier)
        return cleaned_qualifiers
