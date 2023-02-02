from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "bus_station.command_terminal.middleware.command_middleware_receiver.CommandMiddlewareReceiver",
            "bus_station.command_terminal.middleware.command_middleware_receiver.CommandMiddlewareReceiver",
        )
    )
