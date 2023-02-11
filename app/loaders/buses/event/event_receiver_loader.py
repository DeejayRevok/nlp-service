from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "bus_station.event_terminal.middleware.event_middleware_receiver.EventMiddlewareReceiver",
            "bus_station.event_terminal.middleware.event_middleware_receiver.EventMiddlewareReceiver",
        )
    )
