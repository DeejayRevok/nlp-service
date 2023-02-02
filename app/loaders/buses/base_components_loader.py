from bus_station.shared_terminal.bus_stop_resolver.pypendency_bus_stop_resolver import PypendencyBusStopResolver
from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "bus_station.passengers.passenger_record.in_memory_passenger_record_repository.InMemoryPassengerRecordRepository",
            "bus_station.passengers.passenger_record.in_memory_passenger_record_repository.InMemoryPassengerRecordRepository",
        )
    )
    container_builder.set_definition(
        Definition(
            "bus_station.passengers.passenger_record.redis_passenger_record_repository.RedisPassengerRecordRepository",
            "bus_station.passengers.passenger_record.redis_passenger_record_repository.RedisPassengerRecordRepository",
            [
                Argument.no_kw_argument("@redis.Redis"),
            ]
        )
    )
    container_builder.set_definition(
        Definition(
            "bus_station.shared_terminal.fqn_getter.FQNGetter",
            "bus_station.shared_terminal.fqn_getter.FQNGetter",
        )
    )
    container_builder.set_definition(
        Definition(
            "bus_station.passengers.passenger_class_resolver.PassengerClassResolver",
            "bus_station.passengers.passenger_class_resolver.PassengerClassResolver"
        )
    )
    container_builder.set_definition(
        Definition(
            "bus_station.passengers.serialization.passenger_json_serializer.PassengerJSONSerializer",
            "bus_station.passengers.serialization.passenger_json_serializer.PassengerJSONSerializer"
        )
    )
    container_builder.set(
        "bus_station.shared_terminal.bus_stop_resolver.pypendency_bus_stop_resolver.PypendencyBusStopResolver",
        PypendencyBusStopResolver(container_builder)
    )
