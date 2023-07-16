from app.loaders.buses.command.sync_command_bus_loader import load as load_sync_command_bus


def load() -> None:
    load_sync_command_bus()
