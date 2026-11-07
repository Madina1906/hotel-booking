"""Notifications module: tells guests what happened. Public contract only; senders are in internal.py."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass(frozen=True)
class Confirmation:
    """The five fields of ReservationConfirmed. Nothing else crosses the border."""

    reservation_id: str
    guest_email: str
    room_number: str
    check_in: date
    check_out: date


class NotificationSender(Protocol):
    def send_confirmation(self, confirmation: Confirmation) -> None: ...


__all__ = ["Confirmation", "NotificationSender"]
