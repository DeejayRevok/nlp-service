"""
Celery tasks implementation module
"""
from celery.signals import worker_process_init, worker_process_shutdown
from pypendency.builder import container_builder

from news_service_lib.messaging import ExchangePublisher
from news_service_lib.models import New, NamedEntity

from config import config
from log_config import get_logger
from worker.main import CELERY_APP
from worker.utils.chained_task import ChainedTask

LOGGER = get_logger()


@worker_process_init.connect()
def initialize_worker(*_, **__):
    """
    Initialize the celery worker global variables
    """
    LOGGER.info('Initializing worker')
    exchange_publisher: ExchangePublisher = container_builder.get('exchange_publisher')
    exchange_publisher.connect()
    exchange_publisher.initialize()


@CELERY_APP.app.task(name='process_new_content', base=ChainedTask)
def process_new_content(new: dict = None, **_):
    """
    Apply NLP processing to the input new content

    Args:
        new: new to process content

    Returns: new to hydrate in next tasks, processed new content

    """
    LOGGER.info('NLP Processing new %s', new['title'])

    nlp_service = container_builder.get('services.nlp_service.NlpService')
    if nlp_service is not None:
        processed_content = nlp_service.process_text(new['content'])
        return nlp_service.doc_to_json_dict(processed_content)
    else:
        LOGGER.warning('NLP service not initialized, skipping NLP processing')
        return None


@CELERY_APP.app.task(name='summarize', base=ChainedTask)
def summarize(nlp_doc: dict = None, **_):
    """
    Generate the summary for the input NLP doc

    Args:
        nlp_doc: document to generate summary

    Returns: summary of the doc sentences

    """
    LOGGER.info('Generating summary')

    nlp_service = container_builder.get('services.nlp_service.NlpService')
    summarizer = container_builder.get('services.summary_service.SummaryService')
    if summarizer is not None:
        if nlp_doc is not None:
            doc = nlp_service.doc_from_json_dict(nlp_doc)
            return summarizer(list(doc.sents))
        else:
            LOGGER.warning('NLP document is missing. Skipping summary generation...')
            return None
    else:
        LOGGER.warning('Summarizer not initialized. Skipping summary generation...')
        return None


@CELERY_APP.app.task(name='sentiment_analysis', base=ChainedTask)
def sentiment_analysis(nlp_doc: dict = None, **_):
    """
    Get the sentiment score of the input doc sentences

    Args:
        nlp_doc: doc to analyze sentiment

    Returns: input doc sentences sentiment score

    """
    LOGGER.info('Generating sentiment score')

    nlp_service = container_builder.get('services.nlp_service.NlpService')
    sentiment_analyzer = container_builder.get('services.sentiment_analysis_service.SentimentAnalysisService')
    if sentiment_analyzer is not None:
        if nlp_doc is not None:
            doc = nlp_service.doc_from_json_dict(nlp_doc)
            return sentiment_analyzer(list(doc.sents))
        else:
            LOGGER.warning('NLP document is missing. Skipping sentiment calculation...')
            return None
    else:
        LOGGER.warning('Sentiment analyzer not initialized. Skipping sentiment calculation...')
        return None


@CELERY_APP.app.task(name='hydrate_new', base=ChainedTask)
def hydrate_new(new: dict = None, nlp_doc: dict = None, summary: str = None, sentiment: float = None, **_):
    """
    Hydrate the input new with the named entities and noun chunks from the input NLP document and with the input
    summary and sentiment

    Args:
        new: new to hydrate
        nlp_doc: new NLP information
        summary: new summary
        sentiment: new sentiment

    Returns: hydrated new

    """
    LOGGER.info('Hydrating new %s', new['title'])
    new = New(**new)

    if summary is not None:
        new.summary = summary

    if sentiment is not None:
        new.sentiment = sentiment

    nlp_service = container_builder.get('services.nlp_service.NlpService')
    if nlp_doc is not None:
        doc = nlp_service.doc_from_json_dict(nlp_doc)
        new.entities = list(
            set(map(lambda entity: NamedEntity(text=str(entity), type=entity.label_), doc.ents)))
        new.noun_chunks = list(map(lambda chunk: str(chunk), doc.noun_chunks))

    return dict(new)


@CELERY_APP.app.task(name='publish_hydrated_new', base=ChainedTask)
def publish_hydrated_new(new: dict = None, **_):
    """
    Publish the the input new updated
    Args:
        new: new to publish
    """
    if new is not None:
        LOGGER.info('Publishing hydrated new %s', new['title'])
        if config.rabbit is not None:
            LOGGER.info('Queue connection initialized, publishing...')

            new['hydrated'] = True
            exchange_publisher: ExchangePublisher = container_builder.get('exchange_publisher')

            exchange_publisher(new)
            LOGGER.info('New published')
        else:
            LOGGER.warning('Queue connection configuration not initialized, skipping publish...')
    else:
        LOGGER.warning('Tasks chain services not initialized, skipping publish...')


@worker_process_shutdown.connect()
def shutdown_worker(*_, **__):
    """
    Shutdown the celery worker shutting down the exchange publisher
    """
    LOGGER.info('Shutting down worker')
    exchange_publisher: ExchangePublisher = container_builder.get('exchange_publisher')
    exchange_publisher.shutdown()
