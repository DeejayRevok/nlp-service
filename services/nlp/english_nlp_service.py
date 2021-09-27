from services.nlp.nlp_service import NLPService


class EnglishNLPService(NLPService):
    def __init__(self):
        super().__init__("en_core_web_md")
