from unittest import TestCase

from services.summary.english_summary_service import EnglishSummaryService
from services.summary.summary_service import initialize_summary_service


class TestEnglishSummaryService(TestCase):

    TEST_INPUT_SENTENCES = [
        "This phrase brings meaning.",
        "Of that and this and that but nothing.",
        "Of that and this and the other phrase but nothing.",
        "A different but very important phrase.",
        "This phrase brings meaning and significance.",
    ]

    OUTPUT_SUMMARY_SENTENCES = ["A different but very important phrase.", "This phrase brings meaning."]
    OUTPUT_SUMMARY_EXCLUDED_SENTENCES = [
        "This phrase brings meaning and significance.",
        "Of that and this and that but nothing.",
        "Of that and this and the other phrase but nothing.",
    ]

    def test_generate_summary_from_sentences(self):
        initialize_summary_service()
        english_summary_service = EnglishSummaryService()
        summary = english_summary_service.summarize(self.TEST_INPUT_SENTENCES)
        for sentence in self.OUTPUT_SUMMARY_SENTENCES:
            self.assertIn(sentence, summary)
        for sentence in self.OUTPUT_SUMMARY_EXCLUDED_SENTENCES:
            self.assertNotIn(sentence, summary)
