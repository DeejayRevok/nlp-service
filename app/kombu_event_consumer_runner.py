from argparse import ArgumentParser
from typing import Dict

from bus_station.event_terminal.bus_engine.kombu_event_bus_engine import KombuEventBusEngine
from bus_station.event_terminal.event_consumer_registry import EventConsumerRegistry
from bus_station.event_terminal.middleware.event_middleware_receiver import EventMiddlewareReceiver
from bus_station.passengers.serialization.passenger_json_deserializer import PassengerJSONDeserializer
from bus_station.shared_terminal.engine.runner.self_process_engine_runner import SelfProcessEngineRunner
from kombu.connection import Connection
from yandil.container import default_container

from app.loaders import load_app


def run() -> None:
    load_app()
    args = __load_args()
    engine = KombuEventBusEngine(
        broker_connection=default_container[Connection],
        event_receiver=default_container[EventMiddlewareReceiver],
        event_consumer_registry=default_container[EventConsumerRegistry],
        event_deserializer=default_container[PassengerJSONDeserializer],
        event_consumer_name=args["consumer"],
    )
    SelfProcessEngineRunner(engine).run()


def __load_args() -> Dict:
    arg_solver = ArgumentParser(description="Event consumer runner")
    arg_solver.add_argument("-c", "--consumer", required=True, help="Event consumer name")

    return vars(arg_solver.parse_args())


if __name__ == "__main__":
    run()
