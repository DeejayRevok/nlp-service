from services.nlp.nlp_service import NLPService


class SpanishNLPService(NLPService):
    def __init__(self):
        super().__init__("es_core_news_md")
