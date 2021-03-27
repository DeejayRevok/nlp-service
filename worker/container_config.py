"""
Worker application container configuration module
"""
from pypendency.argument import Argument
from pypendency.builder import ContainerBuilder
from pypendency.definition import Definition

from config import config
from log_config import get_logger
from news_service_lib.messaging import ExchangePublisher

LOGGER = get_logger()


def load(container_builder: ContainerBuilder):
    """
    Load all the application services in the container

    Args:
        container_builder: container to load services

    """
    container_builder.set_definition(
        Definition(
            "services.nlp_service.NlpService",
            "services.nlp_service.NlpService",
        )
    )

    container_builder.set_definition(
        Definition(
            "services.summary_service.SummaryService",
            "services.summary_service.SummaryService",
        )
    )

    container_builder.set_definition(
        Definition(
            "services.sentiment_analysis_service.SentimentAnalysisService",
            "services.sentiment_analysis_service.SentimentAnalysisService",
            [
                Argument.no_kw_argument("@services.nlp_service.NlpService")
            ]
        )
    )

    container_builder.set('exchange_publisher',
                          ExchangePublisher(**config.rabbit, exchange='news-internal-exchange', logger=LOGGER))
