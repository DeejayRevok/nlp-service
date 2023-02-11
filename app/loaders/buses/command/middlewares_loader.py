from bus_station.command_terminal.middleware.command_middleware_receiver import CommandMiddlewareReceiver
from bus_station.command_terminal.middleware.implementations.logging_command_middleware import LoggingCommandMiddleware
from bus_station.command_terminal.middleware.implementations.timing_command_middleware import TimingCommandMiddleware
from pypendency.builder import container_builder

from infrastructure.apm.apm_command_middleware import APMCommandMiddleware


def load() -> None:
    command_middleware_receiver: CommandMiddlewareReceiver = container_builder.get(
        "bus_station.command_terminal.middleware.command_middleware_receiver.CommandMiddlewareReceiver"
    )
    command_middleware_receiver.add_middleware_definition(
        LoggingCommandMiddleware, container_builder.get("logging.Logger"), lazy=False
    )
    command_middleware_receiver.add_middleware_definition(
        TimingCommandMiddleware, container_builder.get("logging.Logger"), lazy=True
    )
    command_middleware_receiver.add_middleware_definition(
        APMCommandMiddleware, container_builder.get("elasticapm.Client"), lazy=False
    )
