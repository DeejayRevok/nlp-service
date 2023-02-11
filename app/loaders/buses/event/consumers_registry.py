from bus_station.event_terminal.registry.event_registry import EventRegistry
from pypendency.builder import container_builder

from domain.new.new_saved_event import NewSavedEvent


def register() -> None:
    registry: EventRegistry = container_builder.get(
        "bus_station.event_terminal.registry.redis_event_registry.RedisEventRegistry"
    )
    new_saved_consumer = container_builder.get("application.hydrate_new.new_saved_event_consumer.NewSavedEventConsumer")
    registry.register(new_saved_consumer, NewSavedEvent.passenger_name())
