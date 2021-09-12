"""
Worker application container configuration module
"""
from news_service_lib.configurable_container import ConfigurableContainer
from news_service_lib.messaging.exchange_publisher import ExchangePublisher

from config import config
from log_config import get_logger
from services.nlp_service import NlpService
from services.sentiment_analysis_service import SentimentAnalysisService
from services.summary_service import SummaryService

container: ConfigurableContainer = ConfigurableContainer([], config)


def load():
    """
    Load all the application services in the container
    """
    nlp_service = NlpService()
    container.set("nlp_service", nlp_service)
    container.set("summary_service", SummaryService())
    container.set("sentiment_analysis_service", SentimentAnalysisService(nlp_service))
    container.set(
        "exchange_publisher", ExchangePublisher(**config.rabbit, exchange="news-internal-exchange", logger=get_logger())
    )
