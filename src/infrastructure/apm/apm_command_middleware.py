from typing import Optional

from bus_station.command_terminal.command import Command
from bus_station.command_terminal.command_handler import CommandHandler
from bus_station.command_terminal.middleware.command_middleware import CommandMiddleware
from elasticapm import Client


class APMCommandMiddleware(CommandMiddleware):
    def __init__(self, apm_client: Client):
        self.__apm_client = apm_client

    def before_handle(self, passenger: Command, bus_stop: CommandHandler) -> None:
        self.__apm_client.begin_transaction("command")

    def after_handle(self, passenger: Command, bus_stop: CommandHandler,
                     handling_exception: Optional[Exception] = None) -> None:
        transaction_result = "success"
        if handling_exception is not None:
            transaction_result = "error"
            self.__apm_client.capture_exception(
                exc_info=(handling_exception.__class__, handling_exception, handling_exception.__traceback__)
            )
        self.__apm_client.end_transaction(
            f"{passenger.passenger_name()}-{bus_stop.bus_stop_name()}", transaction_result
        )
