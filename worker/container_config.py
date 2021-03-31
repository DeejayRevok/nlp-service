"""
Worker application container configuration module
"""
from pypendency.builder import ContainerBuilder

from config import config
from log_config import get_logger
from news_service_lib.messaging import ExchangePublisher
from services.nlp_service import NlpService
from services.sentiment_analysis_service import SentimentAnalysisService
from services.summary_service import SummaryService


def load(container_builder: ContainerBuilder):
    """
    Load all the application services in the container

    Args:
        container_builder: container to load services

    """
    nlp_service = NlpService()
    container_builder.set("services.nlp_service.NlpService", nlp_service)

    container_builder.set("services.summary_service.SummaryService", SummaryService())

    container_builder.set("services.sentiment_analysis_service.SentimentAnalysisService",
                          SentimentAnalysisService(nlp_service))

    container_builder.set('news_service_lib.messaging.exchange_publisher',
                          ExchangePublisher(**config.rabbit,
                                            exchange='news-internal-exchange',
                                            logger=get_logger()))
