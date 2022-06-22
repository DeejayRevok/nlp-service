import os

from pypendency.builder import container_builder
from redis import Redis


def load() -> None:
    redis_host = os.environ.get("NLP_SERVICE_REDIS__HOST")
    redis_port = os.environ.get("NLP_SERVICE_REDIS__PORT")
    redis_password = os.environ.get("NLP_SERVICE_REDIS__PASSWORD")
    redis_client = Redis(host=redis_host, port=redis_port, password=redis_password)
    container_builder.set("redis.Redis", redis_client)
