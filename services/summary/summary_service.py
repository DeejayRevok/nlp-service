import math
import string
from statistics import mean
from typing import List, Iterator, Tuple, Union

import numpy as np
import networkx as nx
from nltk import download
from nltk.cluster import cosine_distance
from spacy.tokens import Span

from log_config import get_logger

LOGGER = get_logger()


def initialize_summary_service():
    LOGGER.info("Downloading stopwords...")
    download("stopwords")


class SummaryService:

    def __init__(self, stop_words: List[str]):
        self.__stop_words = stop_words

    def summarize(self, sentences: Union[List[str], List[Span]]) -> str:
        LOGGER.info("Generating summary for %d input sentences", len(sentences))

        stop_words = self.__stop_words
        if stop_words is None:
            stop_words = list()

        preprocessed_sentences = list(self.__preprocess_sentences(sentences, stop_words))

        sentence_similarity_matrix = self.__build_similarity_matrix(
            map(lambda prep_sent: prep_sent[0], preprocessed_sentences), stop_words
        )

        sentence_distance_graph = nx.from_numpy_array(sentence_similarity_matrix)
        scores = nx.pagerank(sentence_distance_graph)

        for i, preprocessed_sentence in enumerate(preprocessed_sentences):
            scores[i] = scores[i] * preprocessed_sentence[1]

        summary_sentences_num = round(len(sentences) / 4)
        summary_sentences_num = summary_sentences_num if summary_sentences_num >= 2 else 2
        summary_sentences_num = summary_sentences_num if summary_sentences_num <= 10 else 10

        ranked_scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
        ranked_sentences = list(ranked_scores.keys())
        qualifiers = ranked_sentences[:summary_sentences_num]
        non_qualifiers = ranked_sentences[summary_sentences_num:]

        self.__clean_qualifiers(qualifiers, non_qualifiers, sentence_similarity_matrix, preprocessed_sentences)

        summarize_text_sentences = []
        for i in sorted(qualifiers):
            sentence = sentences[i] if isinstance(sentences[i], str) else str(sentences[i])
            summarize_text_sentences.append(sentence)

        return " ".join(summarize_text_sentences)

    def __preprocess_sentences(
        self, sentences: Union[List[str], List[Span]], stop_words: List[str]
    ) -> Iterator[Tuple[List[str], float]]:
        for sentence in sentences:
            sentence = sentence if isinstance(sentence, str) else str(sentence)
            sentence_words = [
                word.translate(str.maketrans("", "", string.punctuation)).lower() for word in sentence.split(" ")
            ]
            yield sentence_words, self.__get_sentence_entropy(sentence_words, stop_words)

    def __get_sentence_entropy(self, sentence: List[str], stop_words: List[str]) -> float:
        return mean(map(lambda word: 1 if word not in stop_words else 0, sentence))

    def __build_similarity_matrix(self, sentences: Iterator[List[str]], stop_words: List[str]) -> np.ndarray:
        sentences = list(sentences)
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for idx1, _ in enumerate(sentences):
            for idx2, _ in enumerate(sentences):
                if idx1 == idx2:
                    continue
                similarity_matrix[idx1][idx2] = self.__sentence_similarity(
                    sentences[idx1], sentences[idx2], stop_words
                )

        return similarity_matrix

    def __sentence_similarity(self, sent1: List[str], sent2: List[str], stop_words: list) -> int:
        all_words = list(set(sent1 + sent2))

        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

        for word in sent1:
            if word in stop_words:
                continue
            vector1[all_words.index(word)] += 1

        for word in sent2:
            if word in stop_words:
                continue
            vector2[all_words.index(word)] += 1

        result = cosine_distance(vector1, vector2)
        return 1 - result if not math.isnan(result) else 0.0

    def __clean_qualifiers(
        self,
        qualifiers: List[int],
        non_qualifiers: List[int],
        sentence_similarity_matrix: np.ndarray,
        preprocessed_sentences: List[Tuple[List[str], float]],
    ):
        qualifiers_similarity_matrix = sentence_similarity_matrix.take([qualifiers, list(reversed(qualifiers))])
        similar_qualifiers = set(
            map(
                lambda indexes: tuple(sorted(indexes)),
                filter(lambda indexes: len(indexes) > 0, np.where(qualifiers_similarity_matrix > 0.75)),
            )
        )
        if len(non_qualifiers) > 0 and len(similar_qualifiers) > 0:
            for idx1, idx2 in set(map(lambda indexes: tuple(sorted(indexes)), list(similar_qualifiers))):
                if len(non_qualifiers) > 0:
                    if preprocessed_sentences[qualifiers[idx1]][1] >= preprocessed_sentences[qualifiers[idx2]][1]:
                        del qualifiers[idx2]
                    else:
                        del qualifiers[idx1]
                    qualifiers.append(non_qualifiers.pop(0))
            self.__clean_qualifiers(
                qualifiers, non_qualifiers, sentence_similarity_matrix, preprocessed_sentences
            )
