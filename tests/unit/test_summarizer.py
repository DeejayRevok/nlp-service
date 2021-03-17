"""
Summarizer tests module
"""
from unittest import TestCase
from unittest.mock import patch

from services.summary_service import initialize_summary_service, SummaryService


class TestSummarizer(TestCase):
    """
    Summarizer test cases
    """
    TEST_INPUT_SENTENCES = ['Esta frase aporta significado.',
                            'De eso y esto y lo otro pero nada.',
                            'De eso y esto y la otra frase pero nada.',
                            'Una frase diferente pero con mucha importancia.',
                            'Esta frase aporta significado y significado.']

    OUTPUT_SUMMARY_SENTENCES = ['Una frase diferente pero con mucha importancia.',
                                'Esta frase aporta significado.']
    OUTPUT_SUMMARY_EXCLUDED_SENTENCES = ['Esta frase aporta significado y significado.',
                                         'De eso y esto y lo otro pero nada.',
                                         'De eso y esto y la otra frase pero nada.']

    @patch('services.summary_service.download')
    def test_initialize_summarizer(self, download_mock):
        """
        Test the initialize summarizer downloads the required resources
        """
        initialize_summary_service()
        download_mock.assert_called_with('stopwords')

    def test_generate_summary_from_sentences(self):
        """
        Test the summary generation returns the correct summary
        """
        initialize_summary_service()
        summary_service = SummaryService()
        summary = summary_service(self.TEST_INPUT_SENTENCES)
        for sentence in self.OUTPUT_SUMMARY_SENTENCES:
            self.assertIn(sentence, summary)
        for sentence in self.OUTPUT_SUMMARY_EXCLUDED_SENTENCES:
            self.assertNotIn(sentence, summary)
