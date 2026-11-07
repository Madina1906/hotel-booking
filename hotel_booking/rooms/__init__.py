"""Rooms module: knows which rooms the hotel sells. Public contract only; the rest is in internal.py."""
from hotel_booking.rooms.catalog import Room, RoomCatalog

__all__ = ["Room", "RoomCatalog"]
