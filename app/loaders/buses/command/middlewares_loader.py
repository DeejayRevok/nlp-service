from logging import Logger

from bus_station.command_terminal.middleware.command_middleware_receiver import CommandMiddlewareReceiver
from bus_station.command_terminal.middleware.implementations.logging_command_middleware import LoggingCommandMiddleware
from bus_station.command_terminal.middleware.implementations.timing_command_middleware import TimingCommandMiddleware
from elasticapm import Client
from yandil.container import default_container

from infrastructure.apm.apm_command_middleware import APMCommandMiddleware


def load() -> None:
    command_middleware_receiver = default_container[CommandMiddlewareReceiver]
    command_middleware_receiver.add_middleware_definition(
        LoggingCommandMiddleware, default_container[Logger], lazy=False
    )
    command_middleware_receiver.add_middleware_definition(TimingCommandMiddleware, default_container[Logger], lazy=True)
    command_middleware_receiver.add_middleware_definition(APMCommandMiddleware, default_container[Client], lazy=False)
