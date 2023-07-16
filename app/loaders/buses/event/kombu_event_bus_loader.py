from bus_station.event_terminal.bus.asynchronous.distributed.kombu_event_bus import KombuEventBus
from bus_station.event_terminal.event_consumer_registry import EventConsumerRegistry
from bus_station.event_terminal.middleware.event_middleware_receiver import EventMiddlewareReceiver
from yandil.container import default_container


def load() -> None:
    default_container.add(EventMiddlewareReceiver)
    default_container.add(EventConsumerRegistry)
    default_container.add(KombuEventBus)
