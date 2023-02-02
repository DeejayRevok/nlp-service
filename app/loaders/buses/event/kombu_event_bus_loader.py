from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "bus_station.event_terminal.registry.redis_event_registry.RedisEventRegistry",
            "bus_station.event_terminal.registry.redis_event_registry.RedisEventRegistry",
            [
                Argument("redis_repository",
                         "@bus_station.passengers.passenger_record.redis_passenger_record_repository.RedisPassengerRecordRepository"),
                Argument("event_consumer_resolver",
                         "@bus_station.shared_terminal.bus_stop_resolver.pypendency_bus_stop_resolver.PypendencyBusStopResolver"),
                Argument("fqn_getter", "@bus_station.shared_terminal.fqn_getter.FQNGetter"),
                Argument("passenger_class_resolver",
                         "@bus_station.passengers.passenger_class_resolver.PassengerClassResolver")
            ]
        )
    )
    container_builder.set_definition(
        Definition(
            "bus_station.event_terminal.bus.asynchronous.distributed.kombu_event_bus.KombuEventBus",
            "bus_station.event_terminal.bus.asynchronous.distributed.kombu_event_bus.KombuEventBus",
            [
                Argument.no_kw_argument("@kombu.connection.Connection"),
                Argument.no_kw_argument("@bus_station.passengers.serialization.passenger_json_serializer.PassengerJSONSerializer"),
                Argument.no_kw_argument("@bus_station.event_terminal.registry.redis_event_registry.RedisEventRegistry"),
            ]
        )
    )
