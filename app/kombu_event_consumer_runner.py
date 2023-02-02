from argparse import ArgumentParser
from typing import Dict

from bus_station.event_terminal.bus_engine.kombu_event_bus_engine import KombuEventBusEngine
from bus_station.passengers.serialization.passenger_json_deserializer import PassengerJSONDeserializer
from bus_station.shared_terminal.engine.runner.self_process_engine_runner import SelfProcessEngineRunner
from pypendency.builder import container_builder

from app.loaders import load as load_app


def run() -> None:
    load_app()
    args = __load_args()
    engine = KombuEventBusEngine(
        container_builder.get("kombu.connection.Connection"),
        container_builder.get("bus_station.event_terminal.registry.redis_event_registry.RedisEventRegistry"),
        container_builder.get("bus_station.event_terminal.middleware.event_middleware_receiver.EventMiddlewareReceiver"),
        PassengerJSONDeserializer(),
        args["event"],
        args["consumer"]
    )
    SelfProcessEngineRunner(engine).run()


def __load_args() -> Dict:
    arg_solver = ArgumentParser(description="Event consumer runner")
    arg_solver.add_argument("-e", "--event", required=True, help="Event name")
    arg_solver.add_argument("-c", "--consumer", required=True, help="Event consumer name")

    return vars(arg_solver.parse_args())


if __name__ == "__main__":
    run()
