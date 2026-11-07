from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Room:
    number: str
    type: str


class RoomCatalog(Protocol):
    """The promise Rooms makes to the others: "here are the rooms"."""

    def all(self) -> list[Room]: ...
