"""
Main nlp celery worker module
"""
from os.path import dirname, join, abspath

from celery.concurrency import asynpool
from elasticapm import Client
from elasticapm.contrib.celery import register_instrumentation, register_exception_tracking
from pypendency.builder import container_builder
from pypendency.loaders.py_loader import PyLoader
from news_service_lib import profile_args_parser, add_logstash_handler
from news_service_lib.base_celery_app import BaseCeleryApp
from news_service_lib.redis_utils import build_redis_url

from config import load_config, config
from log_config import LOG_CONFIG, get_logger
from services.summary_service import initialize_summary_service

LOGGER = get_logger()
asynpool.PROC_ALIVE_TIMEOUT = 60.0
CELERY_APP = BaseCeleryApp('Nlp service worker', ['worker.celery_tasks'])


def main(profile: str):
    """
    Celery worker main entry point

    Args:
        profile: profile used to run the app

    """
    load_config(profile)
    initialize_summary_service()
    PyLoader(container_builder).load(join(abspath(dirname(__file__)), 'container_config.py'))

    add_logstash_handler(LOG_CONFIG, config.logstash.host, config.logstash.port)
    CELERY_APP.configure(task_queue_name='nlp-worker',
                         broker_config=config.rabbit,
                         worker_concurrency=config.celery.concurrency,
                         result_backend_url=build_redis_url(**config.redis))

    apm_client = Client(config={
        'SERVICE_NAME': config.elastic_apm.service_name,
        'SECRET_TOKEN': config.elastic_apm.secret_token,
        'SERVER_URL': f'http://{config.elastic_apm.host}:{config.elastic_apm.port}'
    })
    register_instrumentation(apm_client)
    register_exception_tracking(apm_client)

    CELERY_APP.run()


if __name__ == '__main__':
    args = profile_args_parser('NLP Celery worker')
    main(args['profile'])