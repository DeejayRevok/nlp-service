from app.loaders.buses.command.command_receiver_loader import load as load_command_receiver
from app.loaders.buses.command.sync_command_bus_loader import load as load_sync_command_bus

def load() -> None:
    load_command_receiver()
    load_sync_command_bus()
