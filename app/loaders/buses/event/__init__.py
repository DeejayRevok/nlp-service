from app.loaders.buses.event.kombu_event_bus_loader import load as load_kombu_event_bus
from app.loaders.buses.event.passenger_loader import load as load_event_passengers


def load() -> None:
    load_event_passengers()
    load_kombu_event_bus()
