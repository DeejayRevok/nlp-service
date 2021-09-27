from nltk.corpus import stopwords

from services.summary.summary_service import SummaryService


class SpanishSummaryService(SummaryService):
    def __init__(self):
        super().__init__(stopwords.words("spanish"))
