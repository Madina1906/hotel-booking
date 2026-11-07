# ADR-001: Modular monolith with four modules

Status: Accepted (7 November 2026)

## Context
The hotel app has four areas (Rooms, Reservations, Payments, Notifications) that grew together in one codebase. A change to one area (for example a new SMS sender) risks breaking the others, and nothing stops one area from reaching into another's internals. The team is small and the app is deployed as one unit.

## Decision
We keep one deployable application (a monolith) and split its code into four modules, one per context. Each module has a public contract (what others may use) and internal code (what only the module, the wiring in main.py and the tests may use). Other modules depend on contracts, never on internal code. We check the borders automatically with import-linter, three rules in pyproject.toml.

## Consequences
- Good: one area can change without touching the others; the borders are checked by a tool, not by memory; one deployment stays simple.
- Good: a module can later move into its own service, because its contract is already the boundary.
- Bad: a little more code (contracts such as Confirmation, extra files).
- Bad: the borders hold only while the checks run on every change.
- Not solved here: the double-booking race stays until P09.
