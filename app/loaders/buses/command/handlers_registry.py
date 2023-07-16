from bus_station.command_terminal.command_handler_registry import CommandHandlerRegistry
from yandil.container import default_container

from application.hydrate_new.hydrate_new_command_handler import HydrateNewCommandHandler


def register() -> None:
    registry = default_container[CommandHandlerRegistry]
    registry.register(default_container[HydrateNewCommandHandler])
