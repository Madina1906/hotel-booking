from __future__ import annotations

from decimal import Decimal

from hotel_booking.payments import PaymentStatus


class SimulatedPaymentService:
    """Internal to Payments: pays any positive amount. A real provider arrives in P17."""

    def take_deposit(self, reservation_id: str, amount: Decimal) -> PaymentStatus:
        return PaymentStatus.PAID if amount > 0 else PaymentStatus.DECLINED
