# Hotel contexts

## Words

| Word | Meaning here | Name in our code |
|---|---|---|
| Stay | Check-in to check-out, half-open: 12–14 Nov = the nights of the 12th and 13th | DateRange |
| Reservation | Guest + room + stay + status, with an id such as R101 | Reservation |
| Confirmed | The room is promised to this guest for these nights | ReservationStatus.CONFIRMED |
| Guest | The person who stays; has a name and an email address (Maya, maya@example.com) | Guest |
| Room | One physical room the hotel sells, with a number and a type (R8: Deluxe) | Room |
| Room type | The category of a room, such as Standard or Deluxe | Room.type |
| Nightly price | What one night in a room costs; depends on the room type | not in code yet |
| Out of service | A room that is temporarily not for sale, for example R8 under repair | not in code yet |
| Cancelled | The promise is withdrawn; the nights are free again | ReservationStatus.CANCELLED |
| Book | Ask for a room for some nights; the answer is Accepted, Unavailable or InvalidDates | BookingService.reserve |
| Cancel | Withdraw a reservation by its id, for example R101 | BookingService.cancel |
| Free rooms | The rooms that no Confirmed reservation blocks for the asked nights | BookingService.find_free_rooms |
| Deposit | 30% of the stay's price, taken when the guest books | not in code yet |
| Paid | The deposit has arrived | not in code yet |
| Declined | The payment provider refused the deposit | not in code yet |
| Confirmation message | The email or SMS that tells the guest "R101 is confirmed" | NotificationSender.send_confirmation |
| Sent | The message left the hotel and reached the provider | not in code yet |
| Failed | The message could not be sent (the mail server is down) | not in code yet |

## Rooms

Job: knows which rooms the hotel sells.

| Word | Meaning here |
|---|---|
| Room | One physical room the hotel sells, with a number and a type (R8: Deluxe) |
| Room type | The category of a room, such as Standard or Deluxe |
| Nightly price | What one night in a room costs; depends on the room type |
| Out of service | A room that is temporarily not for sale, for example R8 under repair |

Rules this context owns:
- A room that is out of service is not offered to guests.
- The nightly price depends on the room type (Deluxe costs more than Standard).

Needs from other contexts: nothing.
Tells other contexts: nothing by itself; it only answers Reservations' question "which rooms exist?".

## Reservations

Job: decides whether a guest gets a room for some nights, and keeps every reservation.

| Word | Meaning here |
|---|---|
| Stay | Check-in to check-out, half-open: 12–14 Nov = the nights of the 12th and 13th |
| Reservation | Guest + room number + stay + status, with an id such as R101 |
| Confirmed | The room is promised to this guest for these nights |
| Cancelled | The promise is withdrawn; the nights are free again |
| Guest | The person who stays; has a name and an email address (Maya, maya@example.com) |
| Book | Ask for a room for some nights; the answer is Accepted, Unavailable or InvalidDates |
| Cancel | Withdraw a reservation by its id, for example R101 |
| Free rooms | The rooms that no Confirmed reservation blocks for the asked nights |

Rules this context owns:
- A room never has two Confirmed reservations that share a night.
- Check-out must be after check-in.
- Cancelling a reservation frees its nights for new bookings.

Needs from other contexts: the list of rooms (Rooms); from P17 also a taken deposit (Payments).
Tells other contexts: ReservationConfirmed (Notifications).

## Payments

Job: takes deposits and records whether they were paid.

| Word | Meaning here |
|---|---|
| Deposit | 30% of the stay's price, taken when the guest books |
| Paid | The deposit has arrived |
| Declined | The payment provider refused the deposit |

Rules this context owns:
- The deposit is 30% of the stay's price.
- Only a Paid deposit can be refunded.

Needs from other contexts: nothing; the reservation id and the amount arrive with Reservations' request.
Tells other contexts: the answer Paid or Declined to Reservations.

## Notifications

Job: tells guests what happened, by email or SMS.

| Word | Meaning here |
|---|---|
| Confirmation message | The email or SMS that tells the guest "R101 is confirmed" |
| Sent | The message left the hotel and reached the provider |
| Failed | The message could not be sent (the mail server is down) |

Rules this context owns:
- A failed message is recorded as Failed and never changes the reservation.

Needs from other contexts: the five fields of ReservationConfirmed (Reservations).
Tells other contexts: nothing.

## Same word, different meaning

| Word | Rooms | Reservations | Payments | Notifications |
|---|---|---|---|---|
| Status | In service / out of service | Confirmed / Cancelled | Paid / Declined | Sent / Failed |
| Room | R8: Deluxe, nightly price, may be out of service | Just the number R8 on a reservation | Not used | Text in the message: "Room R8" |
| Cancel | Take a room off sale | Withdraw a reservation (R101 becomes Cancelled) | Refund a deposit | Not used |

If Notifications could change a reservation's status to Failed, a failed SMS would overwrite Confirmed and Maya would lose R7 because of a message, which breaks rule R6 (a failed message never changes the booking).

## Rule owners

| Card | Rule | Owner | Why this owner |
|---|---|---|---|
| 1 | A room never has two Confirmed reservations that share a night. | Reservations | It keeps every reservation of the room, so it can check them all together. |
| 2 | Check-out must be after check-in. | Reservations | The stay is its word, and it refuses wrong dates before anything else. |
| 3 | Cancelling a reservation frees its nights for new bookings. | Reservations | Only Confirmed reservations block; Cancelled ones do not, and it keeps the statuses. |
| 4 | A room that is out of service is not offered to guests. | Rooms | It knows which rooms are on sale. |
| 5 | The nightly price depends on the room type (Deluxe costs more than Standard). | Rooms | It keeps each room's type and price. |
| 6 | The deposit is 30% of the stay's price. | Payments | Money rules belong to Payments; Reservations hands it the amount, which comes from the nightly price kept by Rooms. |
| 7 | Only a Paid deposit can be refunded. | Payments | It keeps the payment status. |
| 8 | A failed message is recorded as Failed and never changes the reservation. | Notifications | It keeps the message status (rule R6). |

## Between contexts

### Reservations → Notifications: ReservationConfirmed (event)

Sent when: a reservation is saved as Confirmed.

Fields:
- reservationId: R101
- guestEmail: maya@example.com
- roomNumber: R7
- checkIn: 2026-11-12
- checkOut: 2026-11-14

Reservations does not wait for an answer. A failed message never changes R101 (rule R6).

Never crosses: Reservations' list of reservations. Notifications never reads it.

### Reservations → Rooms: which rooms exist? (question)

Sent when: a guest searches free rooms, and when a guest books a room.

What Reservations sends: the question "which rooms exist?" with no other data.

The answer and its fields:
- number: R7, R8
- type: Standard, Deluxe

Reservations waits for the list. Rooms never asks about reservations, so there is no arrow back.

Never crosses: any reservation, guest or stay. Rooms never sees who has booked what.

### Reservations → Payments: take a deposit (question, from P17)

Sent when: a booking is made and a deposit is needed (from P17).

What Reservations sends:
- reservationId: R101
- amount: 30% of the stay's price

The answer and its fields: Paid or Declined. Reservations decides what that answer means for the booking.

Never crosses: the guest's name, the stay dates and the list of reservations. Payments owns money only, and a Paid deposit never decides whether R7 is free.
