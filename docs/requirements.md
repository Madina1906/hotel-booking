# Requirements: hotel booking app, version 1

Rule for dates: a stay counts nights, not days. Check-in day is included, check-out day is not (half-open range). A guest who books 12–14 November sleeps the nights of the 12th and 13th and leaves on the 14th.

## R1 · Search
A guest or receptionist can list the rooms that are free for given dates.
Check: empty hotel, 12–14 November → R7, R8.
Proof: Free rooms 12-14 Nov: R7, R8

## R2 · Book
A guest or receptionist can book a free room. The app answers with a reservation id.
Check: Maya books R7 for 12–14 November → Accepted R101.
Proof: Maya books R7 12-14 Nov: Accepted R101

## R3 · No conflicts
A room never has two confirmed reservations for the same night. Check-out day must be after check-in day.
Check: Omar asks for R7 13–15 November → Unavailable. 15–15 → InvalidDates.
Proof: Omar books R7 13-15 Nov: Unavailable
Proof: Omar books R8 15-15 Nov: InvalidDates

More examples:
- Maya has R7 12–14. Omar asks for R7 13–15 → Unavailable (night of the 13th is shared).
- Maya has R7 12–14. Nora asks for R7 14–16 → Accepted (no shared night; Maya leaves on the 14th).
- Maya has R7 12–14. Maya's own R7 12–14 asked again → Unavailable (nights 12 and 13 are shared).
- R8 is already booked 20–22 November. A request for R8 22–24 November → Accepted (no shared night; the 22nd is check-out day).
- R8 is already booked 20–22 November. A request for R8 21–23 November → Unavailable (night of the 21st is shared).

## R4 · Cancel
A reservation can be cancelled. It stays stored as Cancelled and no longer blocks the room.
Check: Maya cancels R101 → R7 is free again for 12–14 November.
Proof: Maya cancels R101: True
Proof: Free rooms 12-14 Nov: R7, R8 (after the cancellation)

## R5 · View
A reservation can be looked up by its id.
Check: R101 → Maya, R7, 12–14 November, Confirmed.
Proof: `store.find("R101")` returns the reservation with guest Maya, room R7, stay 12–14 Nov, status Confirmed (before it is cancelled).

## R6 · Failed message
If the confirmation cannot be sent, the booking stays saved and Accepted, and the failure is reported.
Check: the mail server is down when Maya books R7 for 12–14 November → the result is still Accepted R101, `notification_failed` is true and the store still holds 1 reservation.
Proof: test `test_a_failed_confirmation_keeps_the_booking` passes (it was red before `reserve` handled the error).
