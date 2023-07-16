from logging import Logger

from bus_station.event_terminal.middleware.event_middleware_receiver import EventMiddlewareReceiver
from bus_station.event_terminal.middleware.implementations.logging_event_middleware import LoggingEventMiddleware
from bus_station.event_terminal.middleware.implementations.timing_event_middleware import TimingEventMiddleware
from elasticapm import Client
from yandil.container import default_container

from infrastructure.apm.apm_event_middleware import APMEventMiddleware


def load() -> None:
    event_middleware_receiver = default_container[EventMiddlewareReceiver]
    event_middleware_receiver.add_middleware_definition(LoggingEventMiddleware, default_container[Logger], lazy=False)
    event_middleware_receiver.add_middleware_definition(TimingEventMiddleware, default_container[Logger], lazy=True)
    event_middleware_receiver.add_middleware_definition(APMEventMiddleware, default_container[Client], lazy=False)
