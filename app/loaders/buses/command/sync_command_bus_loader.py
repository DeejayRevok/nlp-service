from bus_station.command_terminal.bus.synchronous.sync_command_bus import SyncCommandBus
from bus_station.command_terminal.command_handler_registry import CommandHandlerRegistry
from bus_station.command_terminal.middleware.command_middleware_receiver import CommandMiddlewareReceiver
from yandil.container import default_container


def load() -> None:
    default_container.add(CommandMiddlewareReceiver)
    default_container.add(CommandHandlerRegistry)
    default_container.add(SyncCommandBus, is_primary=True)
