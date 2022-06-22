from bus_station.command_terminal.bus.command_bus import CommandBus
from bus_station.event_terminal.event_consumer import EventConsumer

from application.hydrate_new.hydrate_new_command import HydrateNewCommand
from domain.new.new_saved_event import NewSavedEvent


class NewSavedEventConsumer(EventConsumer):
    def __init__(self, command_bus: CommandBus):
        self.__command_bus = command_bus

    def consume(self, event: NewSavedEvent) -> None:
        if event.hydrated is True:
            return
        
        self.__command_bus.transport(
            self.__create_command_from_event(event)
        )

    def __create_command_from_event(self, event: NewSavedEvent) -> HydrateNewCommand:
        return HydrateNewCommand(
            title=event.title,
            url=event.url,
            content=event.content,
            source=event.source,
            date=event.date,
            language=event.language,
            image=event.image
        )

    @classmethod
    def bus_stop_name(cls) -> str:
        return "event_consumer.nlp_service.hydrate_new.new_saved"
