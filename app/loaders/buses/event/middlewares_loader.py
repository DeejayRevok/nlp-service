from bus_station.event_terminal.middleware.event_middleware_receiver import EventMiddlewareReceiver
from bus_station.event_terminal.middleware.implementations.logging_event_middleware import LoggingEventMiddleware
from bus_station.event_terminal.middleware.implementations.timing_event_middleware import TimingEventMiddleware
from pypendency.builder import container_builder

from infrastructure.apm.apm_event_middleware import APMEventMiddleware


def load() -> None:
    event_middleware_receiver: EventMiddlewareReceiver = container_builder.get(
        "bus_station.event_terminal.middleware.event_middleware_receiver.EventMiddlewareReceiver"
    )
    event_middleware_receiver.add_middleware_definition(
        LoggingEventMiddleware, container_builder.get("logging.Logger"), lazy=False
    )
    event_middleware_receiver.add_middleware_definition(
        TimingEventMiddleware, container_builder.get("logging.Logger"), lazy=True
    )
    event_middleware_receiver.add_middleware_definition(
        APMEventMiddleware, container_builder.get("elasticapm.Client"), lazy=False
    )
