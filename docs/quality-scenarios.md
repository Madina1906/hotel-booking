# Quality scenarios

## Stakeholders

| Who | What they care about |
|---|---|
| Guest | Finds a free room quickly; never loses a booking |
| Receptionist | Never promises one room twice; can cancel at the desk |
| Hotel manager (domain expert) | Knows the rules; wants deposits and SMS soon |
| Development team | Can change one area without breaking the others |
| Email/SMS and payment providers | Outside systems that can be slow or down |

## S1 · Performance: free-room search stays fast

| Part | S1 |
|---|---|
| Source | 200 guests |
| Stimulus | They search free rooms for 12–14 Nov |
| Environment | Within one minute |
| Artifact | The free-room search in BookingService (`find_free_rooms`) |
| Response | Every guest gets the correct free rooms |
| Measure | p95 response ≤ 1 second |
| Checked in | P08 (cache), P23 (load test) |

## S2 · Data integrity: no double bookings

| Part | S2 |
|---|---|
| Source | 100 pairs of guests |
| Stimulus | Each pair books the same room and nights at the same moment |
| Environment | Normal opening hours, all pairs at once |
| Artifact | BookingService.reserve and the reservation store |
| Response | Exactly one Confirmed reservation per pair |
| Measure | 0 double bookings (100 pairs → 100 Confirmed reservations, not 200) |
| Checked in | P09 |

## S3 · Availability: a failed message keeps the booking

| Part | S3 |
|---|---|
| Source | The email provider |
| Stimulus | It stops answering |
| Environment | For 10 minutes, during normal bookings |
| Artifact | BookingService.Reserve and the notification sender |
| Response | Every valid booking is still Accepted and saved; the failed message is reported |
| Measure | 0 lost bookings; every failed message is counted |
| Checked in | P04 (R6 test, done) and P10 |

## S4 · Security: nobody reads another guest's reservation

| Part | S4 |
|---|---|
| Source | A guest who is not the owner of the reservation |
| Stimulus | Tries 100 times to read another guest's reservation |
| Environment | Normal operation, logged in as an ordinary guest |
| Artifact | Looking up a reservation by id (the reservation store and the API in front of it) |
| Response | Every attempt is refused; no reservation data is returned |
| Measure | 0 reservations shown to the wrong guest (out of 100 attempts) |
| Checked in | P21 |

## S5 · Modifiability: adding SMS does not touch the booking rules

| Part | S5 |
|---|---|
| Source | The hotel (the manager asks for a new feature) |
| Stimulus | The hotel adds SMS confirmations |
| Environment | At development time, with the 8 tests in place |
| Artifact | BookingService and the notification sender |
| Response | A new sender class is added; BookingService is not edited |
| Measure | 0 edits to BookingService; at most 2 files change |
| Checked in | P04 (SMS sender, done) |

## S6 · Sustainability: less energy for the same searches

| Part | S6 |
|---|---|
| Source | The development team (a change to the app, for example a cache) |
| Stimulus | The same 1,000 searches are run before and after the change |
| Environment | The same server and the same free-room searches |
| Artifact | The free-room search and the storage behind it |
| Response | The server uses less energy for the same useful work |
| Measure | At least 20% fewer watt-hours per 1,000 completed searches |
| Checked in | P08, P24 |
