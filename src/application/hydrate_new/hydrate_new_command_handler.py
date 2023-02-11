from logging import Logger

from bus_station.command_terminal.command_handler import CommandHandler
from bus_station.event_terminal.bus.event_bus import EventBus

from domain.new.language import Language
from domain.new.new import New
from application.hydrate_new.hydrate_new_command import HydrateNewCommand
from domain.new.new_hydrated_event import NewHydratedEvent
from domain.new.new_hydrater import NewHydrater


class HydrateNewCommandHandler(CommandHandler):
    def __init__(self, new_hydrater: NewHydrater, event_bus: EventBus, logger: Logger):
        self.__new_hydrater = new_hydrater
        self.__event_bus = event_bus
        self.__logger = logger

    def handle(self, command: HydrateNewCommand) -> None:
        self.__logger.info(f"Starting new {command.title} hydration")

        new = self.__create_new_from_command(command)
        self.__new_hydrater.hydrate(new)

        new_hydrated_event = self.__create_event_from_new(new)
        self.__event_bus.transport(new_hydrated_event)

        self.__logger.info(f"Finished new {command.title} hydration")

    def __create_event_from_new(self, new: New) -> NewHydratedEvent:
        return NewHydratedEvent(
            title=new.title,
            url=new.url,
            content=new.content,
            source=new.source,
            date=new.date,
            language=new.language.value,
            hydrated=new.hydrated,
            entities=new.entities,
            summary=new.summary,
            sentiment=new.sentiment,
            image=new.image,
        )

    def __create_new_from_command(self, command: HydrateNewCommand) -> New:
        return New(
            title=command.title,
            url=command.url,
            content=command.content,
            source=command.source,
            date=command.date,
            language=Language(command.language),
            hydrated=False,
            image=command.image,
        )

    @classmethod
    def bus_stop_name(cls) -> str:
        return "command_handler.nlp_service.hydrate_new"
