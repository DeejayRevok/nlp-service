from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.hydrate_new.hydrate_new_command_handler.HydrateNewCommandHandler",
            "application.hydrate_new.hydrate_new_command_handler.HydrateNewCommandHandler",
            [
                Argument.no_kw_argument("@domain.new.new_hydrater.NewHydrater"),
                Argument.no_kw_argument(
                    "@bus_station.event_terminal.bus.asynchronous.distributed.kombu_event_bus.KombuEventBus"),
                Argument.no_kw_argument("@logging.Logger"),
            ]
        )
    )
    container_builder.set_definition(
        Definition(
            "application.hydrate_new.new_saved_event_consumer.NewSavedEventConsumer",
            "application.hydrate_new.new_saved_event_consumer.NewSavedEventConsumer",
            [
                Argument.no_kw_argument("@bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus")
            ]
        )
    )
