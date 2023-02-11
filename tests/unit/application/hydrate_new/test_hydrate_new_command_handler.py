from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

from domain.new.new_hydrated_event import NewHydratedEvent

from domain.new.language import Language

from domain.new.new import New

from application.hydrate_new.hydrate_new_command import HydrateNewCommand
from bus_station.event_terminal.bus.event_bus import EventBus

from domain.new.new_hydrater import NewHydrater

from application.hydrate_new.hydrate_new_command_handler import HydrateNewCommandHandler


class TestHydrateNewCommandHandler(TestCase):
    def setUp(self) -> None:
        self.new_hydrater_mock = Mock(spec=NewHydrater)
        self.event_bus_mock = Mock(spec=EventBus)
        self.logger_mock = Mock(spec=Logger)
        self.command_handler = HydrateNewCommandHandler(self.new_hydrater_mock, self.event_bus_mock, self.logger_mock)

    def test_handle_success(self):
        test_command = HydrateNewCommand(
            title="test_title",
            url="test_url",
            content="test_content",
            source="test_source",
            date=42432.89,
            language="english",
            image="test_image",
        )

        self.command_handler.handle(test_command)

        self.new_hydrater_mock.hydrate.assert_called_once_with(
            New(
                title="test_title",
                url="test_url",
                content="test_content",
                source="test_source",
                date=42432.89,
                language=Language.ENGLISH,
                image="test_image",
                hydrated=False,
            )
        )
        self.event_bus_mock.transport.assert_called_once_with(
            NewHydratedEvent(
                title="test_title",
                url="test_url",
                content="test_content",
                source="test_source",
                date=42432.89,
                language="english",
                image="test_image",
                entities=[],
                hydrated=False,
            )
        )
