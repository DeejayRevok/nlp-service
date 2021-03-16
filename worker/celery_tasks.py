"""
Celery tasks implementation module
"""
import json
from typing import Optional

from celery.signals import worker_process_init
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from spacy.tokens import Doc
from news_service_lib.models import New, NamedEntity

from config import config
from log_config import get_logger
from services.nlp_service import NlpService
from services.sentiment_analysis_service import SentimentAnalysisService
from services.summary_service import SummaryService
from worker.celery_app import CELERY_APP
from worker.utils.chained_task import ChainedTask

LOGGER = get_logger()
NLP_SERVICE: Optional[NlpService] = None
SENTIMENT_ANALYZER: Optional[SentimentAnalysisService] = None
SUMMARIZER: Optional[SummaryService] = None


@worker_process_init.connect()
def initialize_worker(*_, **__):
    """
    Initialize the celery worker global variables
    """
    global NLP_SERVICE, SENTIMENT_ANALYZER, SUMMARIZER
    LOGGER.info('Initializing worker')

    NLP_SERVICE = NlpService()
    SENTIMENT_ANALYZER = SentimentAnalysisService(NLP_SERVICE)
    SUMMARIZER = SummaryService()


@CELERY_APP.app.task(name='process_new_content', base=ChainedTask)
def process_new_content(new: dict):
    """
    Apply NLP processing to the input new content

    Args:
        new: new to process content

    Returns: new to hydrate in next tasks, processed new content

    """
    global NLP_SERVICE
    LOGGER.info('NLP Processing new %s', new['title'])
    if NLP_SERVICE is not None:
        processed_content = NLP_SERVICE.process_text(new['content'])
        return processed_content.to_dict()
    else:
        LOGGER.warning('NLP service not initialized, skipping NLP processing')
        return None


@CELERY_APP.app.task(name='summarize', base=ChainedTask)
def summarize(nlp_doc: dict):
    """
    Generate the summary for the input NLP doc

    Args:
        nlp_doc: document to generate summary

    Returns: summary of the doc sentences

    """
    global NLP_SERVICE, SUMMARIZER
    LOGGER.info('Generating summary')
    if SUMMARIZER is not None:
        if nlp_doc is not None:
            doc = Doc(NLP_SERVICE.nlp_vocab()).from_dict(nlp_doc)
            return SUMMARIZER(doc.sents)
        else:
            LOGGER.warning('NLP document is missing. Skipping summary generation...')
            return None
    else:
        LOGGER.warning('Summarizer not initialized. Skipping summary generation...')
        return None


@CELERY_APP.app.task(name='sentiment_analysis', base=ChainedTask)
def sentiment_analysis(nlp_doc: dict):
    """
    Get the sentiment score of the input doc sentences

    Args:
        nlp_doc: doc to analyze sentiment

    Returns: input doc sentences sentiment score

    """
    global SENTIMENT_ANALYZER, NLP_SERVICE
    LOGGER.info('Generating sentiment score')
    if SENTIMENT_ANALYZER is not None:
        if nlp_doc is not None:
            doc = Doc(NLP_SERVICE.nlp_vocab()).from_dict(nlp_doc)
            return SENTIMENT_ANALYZER(doc.sents)
        else:
            LOGGER.warning('NLP document is missing. Skipping sentiment calculation...')
            return None
    else:
        LOGGER.warning('Sentiment analyzer not initialized. Skipping sentiment calculation...')
        return None


@CELERY_APP.app.task(name='hydrate_new', base=ChainedTask)
def hydrate_new(new: dict, nlp_doc: dict, summary: str, sentiment: float):
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
    global NLP_SERVICE
    LOGGER.info('Hydrating new %s', new['title'])
    new = New(**new)

    if summary is not None:
        new.summary = summary

    if sentiment is not None:
        new.sentiment = sentiment

    if nlp_doc is not None:
        doc = Doc(NLP_SERVICE.nlp_vocab()).from_dict(nlp_doc)
        new.entities = list(
            set(map(lambda entity: NamedEntity(text=str(entity), type=entity.label_), doc.ents)))
        new.noun_chunks = list(map(lambda chunk: str(chunk), doc.noun_chunks))

    return dict(new)


@CELERY_APP.app.task(name='publish_hydrated_new', base=ChainedTask)
def publish_hydrated_new(new: dict):
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
            connection = BlockingConnection(
                ConnectionParameters(host=config.rabbit.host,
                                     port=config.rabbit.port,
                                     credentials=PlainCredentials(config.rabbit.user,
                                                                  config.rabbit.password)))
            channel = connection.channel()
            channel.exchange_declare(exchange='news-internal-exchange', exchange_type='fanout', durable=True)
            channel.basic_publish(exchange='news-internal-exchange', routing_key='', body=json.dumps(dict(new)))

            LOGGER.info('New published')
            channel.close()
            connection.close()
        else:
            LOGGER.warning('Queue connection configuration not initialized, skipping publish...')
    else:
        LOGGER.warning('Tasks chain services not initialized, skipping publish...')
