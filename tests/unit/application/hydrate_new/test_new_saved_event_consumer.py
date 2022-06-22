from unittest import TestCase
from unittest.mock import Mock

from application.hydrate_new.hydrate_new_command import HydrateNewCommand
from bus_station.command_terminal.bus.command_bus import CommandBus
from domain.new.new_saved_event import NewSavedEvent

from application.hydrate_new.new_saved_event_consumer import NewSavedEventConsumer


class TestNewSavedEventConsumer(TestCase):
    def setUp(self) -> None:
        self.command_bus_mock = Mock(spec=CommandBus)
        self.event_consumer = NewSavedEventConsumer(
            self.command_bus_mock
        )

    def test_consume_hydrated(self):
        test_event = NewSavedEvent(
            title="test_new",
            url="test_new_url",
            content="test_new_content",
            source="test_new_source",
            date=323123112.0,
            language="test_new_language",
            hydrated=True,
            image="test_image"
        )

        self.event_consumer.consume(test_event)

        self.command_bus_mock.transport.assert_not_called()

    def test_consume_non_hydrated(self):
        test_event = NewSavedEvent(
            title="test_new",
            url="test_new_url",
            content="test_new_content",
            source="test_new_source",
            date=323123112.0,
            language="test_new_language",
            hydrated=False,
            image="test_image"
        )

        self.event_consumer.consume(test_event)

        self.command_bus_mock.transport.assert_called_once_with(
            HydrateNewCommand(
                title="test_new",
                url="test_new_url",
                content="test_new_content",
                source="test_new_source",
                date=323123112.0,
                language="test_new_language",
                image="test_image"
            )
        )