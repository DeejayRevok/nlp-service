from typing import Optional

from bus_station.query_terminal.middleware.query_middleware import QueryMiddleware
from bus_station.query_terminal.query import Query
from bus_station.query_terminal.query_handler import QueryHandler
from bus_station.query_terminal.query_response import QueryResponse
from elasticapm import Client


class APMQueryMiddleware(QueryMiddleware):
    def __init__(self, apm_client: Client):
        self.__apm_client = apm_client

    def before_handle(self, passenger: Query, bus_stop: QueryHandler) -> None:
        self.__apm_client.begin_transaction("query")

    def after_handle(
        self,
        passenger: Query,
        bus_stop: QueryHandler,
        query_response: QueryResponse,
        handling_exception: Optional[Exception] = None,
    ) -> QueryResponse:
        transaction_result = "success"
        if handling_exception is not None:
            transaction_result = "error"
            self.__apm_client.capture_exception(
                exc_info=(handling_exception.__class__, handling_exception, handling_exception.__traceback__)
            )
        self.__apm_client.end_transaction(
            f"{passenger.passenger_name()}-{bus_stop.bus_stop_name()}", transaction_result
        )
        return query_response
