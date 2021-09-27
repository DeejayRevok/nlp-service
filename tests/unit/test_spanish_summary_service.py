from unittest import TestCase
from unittest.mock import patch

from services.summary.summary_service import initialize_summary_service
from services.summary.spanish_summary_service import SpanishSummaryService


class TestSpanishSummarizer(TestCase):

    TEST_INPUT_SENTENCES = [
        "Esta frase aporta significado.",
        "De eso y esto y lo otro pero nada.",
        "De eso y esto y la otra frase pero nada.",
        "Una frase diferente pero con mucha importancia.",
        "Esta frase aporta significado y significado.",
    ]

    OUTPUT_SUMMARY_SENTENCES = ["Una frase diferente pero con mucha importancia.", "Esta frase aporta significado."]
    OUTPUT_SUMMARY_EXCLUDED_SENTENCES = [
        "Esta frase aporta significado y significado.",
        "De eso y esto y lo otro pero nada.",
        "De eso y esto y la otra frase pero nada.",
    ]

    @patch("services.summary.summary_service.download")
    def test_initialize_summary_service(self, download_mock):
        initialize_summary_service()
        download_mock.assert_called_with("stopwords")

    def test_generate_summary_from_sentences(self):
        initialize_summary_service()
        spanish_summary_service = SpanishSummaryService()
        summary = spanish_summary_service.summarize(self.TEST_INPUT_SENTENCES)
        for sentence in self.OUTPUT_SUMMARY_SENTENCES:
            self.assertIn(sentence, summary)
        for sentence in self.OUTPUT_SUMMARY_EXCLUDED_SENTENCES:
            self.assertNotIn(sentence, summary)
