from __future__ import annotations

from hotel_booking.rooms.catalog import Room


class InMemoryRoomCatalog:
    """Internal to Rooms: a fixed list of rooms. Only main.py and the tests may name it."""

    def __init__(self, rooms: list[Room]) -> None:
        self._rooms = list(rooms)

    def all(self) -> list[Room]:
        return list(self._rooms)
