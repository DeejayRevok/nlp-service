import os
from logging import ERROR

from elasticapm.utils.logging import get_logger
from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    get_logger("elasticapm").setLevel(ERROR)
    apm_secret_token = os.environ.get("NLP_SERVICE_ELASTIC_APM__SECRET_TOKEN")
    apm_url = os.environ.get("NLP_SERVICE_ELASTIC_APM__URL")
    container_builder.set_definition(
        Definition(
            "elasticapm.Client",
            "elasticapm.Client",
            [
                Argument("transactions_ignore_patterns", ["^OPTIONS "]),
                Argument("service_name", "nlp-service"),
                Argument("secret_token", apm_secret_token),
                Argument("server_url", apm_url),
            ],
        )
    )
