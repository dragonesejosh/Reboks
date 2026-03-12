# Reboks

Small helper script for building and opening NUS REBOKS facility booking and schedule URLs.

This repo contains a lightweight Python configuration object (`Config`) plus a CLI entry script (`reboks.py`) that:
- Builds query-string parameters (venue / day / date range / time range)
- Opens the REBOKS **Group Booking** search page for availability
- Opens the **Booking Schedule** page to view existing bookings

## Files

- `reboks.py` — simple CLI. Defines some handy venue aliases (e.g. `field`, `bball`, `mpsh1`–`mpsh6`, `track`, `usc`, `courts`) and opens the booking + schedule pages for each argument passed.
- `config.py` — `Config` class that stores query parameters and provides helpers like `set_venue()`, `set_day()`, `set_date()`, `set_time()`, plus `open_booking()` and `open_schedule()`.
- `filters.py` — lookup tables that map REBOKS numeric filter IDs (activity / venue / etc.) to human-readable names.

## Requirements

- Python 3.x
- A default web browser (the script uses Python’s built-in `webbrowser` module)

No third-party dependencies.

## Usage

### Run with predefined aliases

```bash
python reboks.py field bball mpsh1 track
```

### Run with a numeric venue id

If an argument isn’t a known alias, it’s treated as a venue id:

```bash
python reboks.py 40
```

### What happens

For each argument, the script prints the resolved configuration (venue/day/date/time) and then opens two tabs/windows:

1. Group booking search (availability)
2. Booking schedule (existing bookings)

## Customizing the search

Edit `reboks.py` to change the base search parameters:

```python
base = Config(1).set_date("28 Mar").set_time("8 AM", "3 PM")
```

You can also build your own configs in a Python REPL/script:

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

## Disclaimer

This project is not affiliated with NUS/REBOKS. It simply generates and opens URLs in your browser.