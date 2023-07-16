from bus_station.passengers.serialization.passenger_json_deserializer import PassengerJSONDeserializer
from bus_station.passengers.serialization.passenger_json_serializer import PassengerJSONSerializer
from yandil.container import default_container


def load() -> None:
    default_container.add(PassengerJSONSerializer)
    default_container.add(PassengerJSONDeserializer)
