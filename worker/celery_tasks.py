from dataclasses import asdict

from celery.signals import worker_process_init, worker_process_shutdown
from dacite import from_dict

from news_service_lib.messaging.exchange_publisher import ExchangePublisher
from news_service_lib.models.new import New
from news_service_lib.models.named_entity import NamedEntity

from config import config
from log_config import get_logger
from worker.container_config import container
from worker.main import CELERY_APP
from worker.utils.chained_task import ChainedTask

LOGGER = get_logger()


@worker_process_init.connect()
def initialize_worker(*_, **__):
    LOGGER.info("Initializing worker")
    exchange_publisher: ExchangePublisher = container.get("exchange_publisher")
    exchange_publisher.connect()
    exchange_publisher.initialize()


@CELERY_APP.app.task(name="process_new_content", base=ChainedTask)
def process_new_content(new: dict = None, **_):
    LOGGER.info("NLP Processing new %s", new["title"])

    nlp_manager = container.get("nlp_manager")
    if nlp_manager is not None:
        new_language = new["language"]
        processed_content = nlp_manager.process_text(new_language, new["content"])
        return nlp_manager.doc_to_json_dict(new_language, processed_content)
    else:
        LOGGER.warning("NLP manager not initialized, skipping NLP processing")
        return None


@CELERY_APP.app.task(name="summarize", base=ChainedTask)
def summarize(language: str = None, nlp_doc: dict = None, **_):
    LOGGER.info("Generating summary")

    nlp_manager = container.get("nlp_manager")
    summary_manager = container.get("summary_manager")
    if summary_manager is not None:
        if nlp_doc is not None:
            doc = nlp_manager.doc_from_json_dict(language, nlp_doc)
            return summary_manager.summarize(language, list(doc.sents))
        else:
            LOGGER.warning("NLP document is missing. Skipping summary generation...")
            return None
    else:
        LOGGER.warning("Summarizer not initialized. Skipping summary generation...")
        return None


@CELERY_APP.app.task(name="sentiment_analysis", base=ChainedTask)
def sentiment_analysis(language: str = None, nlp_doc: dict = None, **_):
    LOGGER.info("Generating sentiment score")

    nlp_manager = container.get("nlp_manager")
    sentiment_analysis_manager = container.get("sentiment_analysis_manager")
    if sentiment_analysis_manager is not None:
        if nlp_doc is not None:
            doc = nlp_manager.doc_from_json_dict(language, nlp_doc)
            return sentiment_analysis_manager.analyze(language, list(doc.sents))
        else:
            LOGGER.warning("NLP document is missing. Skipping sentiment calculation...")
            return None
    else:
        LOGGER.warning("Sentiment analyzer not initialized. Skipping sentiment calculation...")
        return None


@CELERY_APP.app.task(name="hydrate_new", base=ChainedTask)
def hydrate_new(new: dict = None, nlp_doc: dict = None, summary: str = None, sentiment: float = None, **_):
    LOGGER.info("Hydrating new %s", new["title"])
    new = from_dict(New, new)

    if summary is not None:
        new.summary = summary

    if sentiment is not None:
        new.sentiment = sentiment

    nlp_manager = container.get("nlp_manager")
    if nlp_doc is not None:
        doc = nlp_manager.doc_from_json_dict(new.language, nlp_doc)
        new.entities = list(set(map(lambda entity: NamedEntity(text=str(entity), type=entity.label_), doc.ents)))
        new.noun_chunks = list(map(lambda chunk: str(chunk), doc.noun_chunks))

    new.hydrated = True

    return asdict(new)


@CELERY_APP.app.task(name="publish_hydrated_new", base=ChainedTask)
def publish_hydrated_new(new: dict = None, **_):
    if new is not None:
        LOGGER.info("Publishing hydrated new %s", new["title"])
        if config.rabbit is not None:
            LOGGER.info("Queue connection initialized, publishing...")

            exchange_publisher: ExchangePublisher = container.get("exchange_publisher")
            exchange_publisher(new)

            LOGGER.info("New published")
        else:
            LOGGER.warning("Queue connection configuration not initialized, skipping publish...")
    else:
        LOGGER.warning("Tasks chain services not initialized, skipping publish...")


@worker_process_shutdown.connect()
def shutdown_worker(*_, **__):
    LOGGER.info("Shutting down worker")
    exchange_publisher: ExchangePublisher = container.get("exchange_publisher")
    exchange_publisher.shutdown()
