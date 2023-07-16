from bus_station.event_terminal.event_consumer_registry import EventConsumerRegistry
from yandil.container import default_container

from application.hydrate_new.new_saved_event_consumer import NewSavedEventConsumer


def register() -> None:
    registry = default_container[EventConsumerRegistry]
    registry.register(default_container[NewSavedEventConsumer])
