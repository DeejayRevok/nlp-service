from news_service_lib.configurable_container import ConfigurableContainer
from news_service_lib.messaging.exchange_publisher import ExchangePublisher
from news_service_lib.models.language import Language

from config import config
from log_config import get_logger
from services.nlp.english_nlp_service import EnglishNLPService
from services.nlp.nlp_manager import NLPManager
from services.nlp.spanish_nlp_service import SpanishNLPService
from services.sentiment_analysis.english_sentiment_analysis_service import EnglishSentimentAnalysisService
from services.sentiment_analysis.sentiment_analysis_manager import SentimentAnalysisManager
from services.sentiment_analysis.spanish_sentiment_analysis_service import SpanishSentimentAnalysisService
from services.summary.english_summary_service import EnglishSummaryService
from services.summary.spanish_summary_service import SpanishSummaryService
from services.summary.summary_manager import SummaryManager

container: ConfigurableContainer = ConfigurableContainer([], config)


def load():
    nlp_services = {
        Language.SPANISH.value: SpanishNLPService(),
        Language.ENGLISH.value: EnglishNLPService(),
    }
    nlp_manager = NLPManager(**nlp_services)
    container.set("nlp_manager", nlp_manager)

    summary_services = {
        Language.SPANISH.value: SpanishSummaryService(),
        Language.ENGLISH.value: EnglishSummaryService(),
    }
    summary_manager = SummaryManager(**summary_services)
    container.set("summary_manager", summary_manager)

    sentiment_analysis_services = {
        Language.SPANISH.value: SpanishSentimentAnalysisService(nlp_services[Language.SPANISH.value]),
        Language.ENGLISH.value: EnglishSentimentAnalysisService(),
    }
    sentiment_analysis_manager = SentimentAnalysisManager(**sentiment_analysis_services)
    container.set("sentiment_analysis_manager", sentiment_analysis_manager)

    container.set(
        "exchange_publisher", ExchangePublisher(**config.rabbit, exchange="news-internal-exchange", logger=get_logger())
    )
