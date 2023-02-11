from domain.new.language import Language


class LanguageNotSupportedException(Exception):
    def __init__(self, language: Language):
        self.language = language
        super().__init__(f"Language {language.value} not supported")
