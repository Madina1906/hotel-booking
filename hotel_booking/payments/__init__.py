"""Payments module: takes deposits. Public contract only; the simulated provider is in internal.py."""
from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Protocol


class PaymentStatus(Enum):
    PAID = "Paid"
    DECLINED = "Declined"


class PaymentService(Protocol):
    def take_deposit(self, reservation_id: str, amount: Decimal) -> PaymentStatus: ...


__all__ = ["PaymentService", "PaymentStatus"]
