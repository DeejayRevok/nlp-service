from bus_station.event_terminal.event import Event
from bus_station.passengers.passenger_mapper import passenger_mapper

from domain.new.new_hydrated_event import NewHydratedEvent
from domain.new.new_saved_event import NewSavedEvent


def load() -> None:
    passenger_mapper(NewHydratedEvent, Event, "event.new_hydrated")
    passenger_mapper(NewSavedEvent, Event, "event.new_saved")
