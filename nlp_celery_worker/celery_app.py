"""
Main nlp celery worker module
"""
from news_service_lib import profile_args_parser, Configuration, ConfigProfile, add_logstash_handler
from news_service_lib.base_celery_app import BaseCeleryApp

from log_config import LOG_CONFIG
from nlp_celery_worker.nlp_helpers.sentiment_analyzer import initialize_sentiment_analyzer
from nlp_celery_worker.nlp_helpers.summarizer import initialize_summarizer
from webapp.definitions import CONFIG_PATH


CELERY_APP = BaseCeleryApp('Nlp service worker', ['nlp_celery_worker.celery_nlp_tasks'])

if __name__ == '__main__':
    ARGS = profile_args_parser('NLP Celery worker')

    initialize_summarizer()
    initialize_sentiment_analyzer()

    CONFIGURATION = Configuration(ConfigProfile[ARGS['profile']], CONFIG_PATH)
    add_logstash_handler(LOG_CONFIG, CONFIGURATION.get('LOGSTASH', 'host'), int(CONFIGURATION.get('LOGSTASH', 'port')))
    CELERY_APP.configure(task_queue_name='nlp-worker',
                         broker_config=CONFIGURATION.get_section('RABBIT'),
                         worker_concurrency=int(CONFIGURATION.get('CELERY', 'concurrency')))
    CELERY_APP.run()
