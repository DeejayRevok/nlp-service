from typing import Optional

from bus_station.event_terminal.event import Event
from bus_station.event_terminal.event_consumer import EventConsumer
from bus_station.event_terminal.middleware.event_middleware import EventMiddleware
from elasticapm import Client


class APMEventMiddleware(EventMiddleware):
    def __init__(self, apm_client: Client):
        self.__apm_client = apm_client

    def before_consume(self, passenger: Event, bus_stop: EventConsumer) -> None:
        self.__apm_client.begin_transaction("event")

    def after_consume(
        self, passenger: Event, bus_stop: EventConsumer, consume_exception: Optional[Exception] = None
    ) -> None:
        transaction_result = "success"
        if consume_exception is not None:
            transaction_result = "error"
            self.__apm_client.capture_exception(
                exc_info=(consume_exception.__class__, consume_exception, consume_exception.__traceback__)
            )
        self.__apm_client.end_transaction(
            f"{passenger.passenger_name()}-{bus_stop.bus_stop_name()}", transaction_result
        )
