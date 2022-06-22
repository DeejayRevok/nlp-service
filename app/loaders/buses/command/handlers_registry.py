from bus_station.command_terminal.registry.command_registry import CommandRegistry
from pypendency.builder import container_builder


def register() -> None:
    registry: CommandRegistry = container_builder.get(
        "bus_station.command_terminal.registry.in_memory_command_registry.InMemoryCommandRegistry"
    )
    save_command_handler = container_builder.get(
        "application.hydrate_new.hydrate_new_command_handler.HydrateNewCommandHandler"
    )
    registry.register(save_command_handler, save_command_handler)
