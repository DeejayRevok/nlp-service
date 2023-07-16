from logging import config as logging_config, getLogger, INFO, Logger

from yandil.container import default_container

__LOG_FILE = "/var/log/nlp-service/nlp-service.log"
__LOG_FORMAT = "%(levelname)s %(asctime)s %(funcName)s %(filename)s %(lineno)d %(message)s"

__BASE_LOG_CONFIG = {
    "version": 1,
    "formatters": {"json": {"class": "pythonjsonlogger.jsonlogger.JsonFormatter", "format": __LOG_FORMAT}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "json", "level": INFO},
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "filename": __LOG_FILE,
            "formatter": "json",
            "level": INFO,
        },
    },
    "loggers": {"base_logger": {"handlers": ["console", "file"], "level": INFO}},
}


def load() -> None:
    logging_config.dictConfig(__BASE_LOG_CONFIG)
    logger = getLogger("base_logger")
    logger.propagate = False
    default_container[Logger] = logger
