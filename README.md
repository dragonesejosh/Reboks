# Reboks

Small helper script for building and opening NUS REBOKS facility booking and schedule URLs.

This repo contains a lightweight Python configuration object (`Config`) plus a CLI entry script (`reboks.py`) that:
- Builds query-string parameters (venue / day / date range / time range)
- Opens the REBOKS **Group Booking** search page for availability
- Opens the **Booking Schedule** page to view existing bookings

## Files

- `reboks.py` — simple CLI. Defines predefined venue aliases and opens the booking + schedule pages for each argument passed.
- `config.py` — `Config` class that stores query parameters and provides helpers like `set_venue()`, `set_day()`, `set_date()`, `set_time()`, plus `open_booking()` and `open_schedule()`.
- `filters.py` — lookup tables (`filters`) that map REBOKS numeric filter IDs (activity / venue / etc.) to human-readable names, plus `opp_filters` for the reverse mapping (name → ID).

## Requirements

- Python 3.x
- A default web browser (the script uses Python's built-in `webbrowser` module)

No third-party dependencies.

## Usage

### Run with predefined aliases

```bash
python reboks.py field bball mpsh1 track
```

Available aliases and their REBOKS venues:

| Alias    | Venue ID | REBOKS Name                                  |
|----------|----------|----------------------------------------------|
| `field`  | 8        | Kent Ridge - Multi-purpose Fields            |
| `bball`  | 2        | Kent Ridge - Outdoor Basketball Courts       |
| `mpsh1`  | 12       | Kent Ridge - Multi-purpose Sports Hall 1     |
| `mpsh2`  | 13       | Kent Ridge - Multi-purpose Sports Hall 2     |
| `mpsh4`  | 14       | Kent Ridge - Multi-purpose Sports Hall 4     |
| `mpsh5`  | 15       | Kent Ridge - Multi-purpose Sports Hall 5     |
| `mpsh6`  | 16       | Kent Ridge - Multi-purpose Sports Hall 6     |
| `track`  | 7        | Kent Ridge - Stadium                         |
| `usc`    | 40       | University Sports Centre - Sports Hall       |
| `courts` | 5        | Kent Ridge - Outdoor Multi-purpose Courts    |

> **Note:** There is no MPSH 3 in REBOKS; the numbering goes MPSH 1, 2, 4, 5, 6.

### Run with a numeric venue ID

If an argument isn't a known alias, it's treated as a raw venue ID:

```bash
python reboks.py 40
```

To discover venue IDs, consult the `filters` list in `filters.py` (index 3 is the venue filter) or use `opp_filters`:

```python
from filters import opp_filters
# opp_filters[3] maps venue names to their numeric IDs
print(opp_filters[3])
```

### What happens

For each argument, the script prints the resolved configuration (venue/day/date/time) and then opens two browser tabs/windows:

1. Group booking search (availability)
2. Booking schedule (existing bookings)

## Customizing the search

Edit `reboks.py` to change the base search parameters (date and time window):

```python
base = Config(1).set_date("28 Mar").set_time("8 AM", "3 PM")
```

You can also build your own configs in a Python REPL or script:

```python
from config import Config

c = (
    Config(8)
    .set_day(2)               # Monday=1 ... Saturday=6
    .set_date("28 Mar 2026")
    .set_time("08:00 AM", "03:00 PM")
)

print(c)
c.open_booking()
c.open_schedule()
```

## Notes

- Dates and times are URL-encoded internally.
- `set_day()` with no argument removes the day filter (search across all days).
- `set_date(date_from, date_to)` accepts a single date or a date range; if only one date is provided it is used for both start and end.

## Disclaimer

This project is not affiliated with NUS/REBOKS. It simply generates and opens URLs in your browser.
