from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "bus_station.command_terminal.registry.in_memory_command_registry.InMemoryCommandRegistry",
            "bus_station.command_terminal.registry.in_memory_command_registry.InMemoryCommandRegistry",
            [
                Argument(
                    "in_memory_repository",
                    "@bus_station.passengers.passenger_record"
                    ".in_memory_passenger_record_repository.InMemoryPassengerRecordRepository",
                ),
                Argument(
                    "command_handler_resolver",
                    "@bus_station.shared_terminal.bus_stop_resolver"
                    ".pypendency_bus_stop_resolver.PypendencyBusStopResolver",
                ),
                Argument("fqn_getter", "@bus_station.shared_terminal.fqn_getter.FQNGetter"),
                Argument(
                    "passenger_class_resolver",
                    "@bus_station.passengers.passenger_class_resolver.PassengerClassResolver",
                ),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus",
            "bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus",
            [
                Argument.no_kw_argument(
                    "@bus_station.command_terminal.registry.in_memory_command_registry.InMemoryCommandRegistry"
                ),
                Argument.no_kw_argument(
                    "@bus_station.command_terminal.middleware.command_middleware_receiver.CommandMiddlewareReceiver"
                ),
            ],
        )
    )
