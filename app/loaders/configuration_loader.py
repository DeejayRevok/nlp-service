from yandil.configuration.configuration_container import default_configuration_container
from yandil.configuration.environment import Environment


def load() -> None:
    default_configuration_container["secret_token"] = Environment("NLP_SERVICE_ELASTIC_APM__SECRET_TOKEN")
    default_configuration_container["server_url"] = Environment("NLP_SERVICE_ELASTIC_APM__URL")
