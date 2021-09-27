from nltk.corpus import stopwords

from services.summary.summary_service import SummaryService


class EnglishSummaryService(SummaryService):
    def __init__(self):
        super().__init__(stopwords.words("english"))
