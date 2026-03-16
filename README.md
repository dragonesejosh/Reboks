# Reboks

Small CLI tool for building and opening NUS REBOKS facility booking and schedule URLs.

This repo contains a lightweight Python configuration object (`Config`) plus a CLI entry script (`reboks.py`) that:
- Builds query-string parameters (venue / day / date range / time range)
- Opens the REBOKS **Group Booking** search page for availability
- Opens the **Booking Schedule** page to view existing bookings

## Files

- `reboks.py` — CLI entry point. Provides two subcommands: `list` (browse available venues) and `search` (open booking/schedule URLs for one or more numeric venue ids).
- `config.py` — `Config` class that stores query parameters and provides helpers like `set_venue()`, `set_day()`, `set_date()`, `set_time()`, plus `open_booking()` and `open_schedule()`.
- `filters.py` — lookup tables that map REBOKS numeric filter IDs (activity / venue / etc.) to human-readable names.
- `parser.py` — helpers for encoding/decoding date and time strings to/from the REBOKS URL format.

## Requirements

- Python 3.8+ (as specified in `pyproject.toml`)
- A default web browser (the script uses Python's built-in `webbrowser` module)
- [`python-dateutil`](https://pypi.org/project/python-dateutil/) for date/time parsing

## Installation

The easiest way to install everything (Python package + all dependencies including `python-dateutil`) is:

```bash
pip install -e .
```

If you only want to run the scripts directly without installing the package, install the dependency manually:

```bash
pip install python-dateutil
```

## Usage

### List all venues

```bash
reboks list
```

Look up specific venue ids:

```bash
reboks list 8 40
```

### Search for a venue

```bash
reboks search 8 --date '28 Mar' --from '8 AM' --to '3 PM'
```

Search multiple venues at once:

```bash
reboks search 8 2 40 --date '28 Mar' --from '8 AM' --to '3 PM'
```

Use a date range instead of a single date:

```bash
reboks search 8 --date-from '28 Mar' --date-to '30 Mar' --from '8 AM' --to '3 PM'
```

Filter by day of week (Monday=1 … Saturday=6):

```bash
reboks search 8 --date '28 Mar' --from '8 AM' --to '3 PM' --day 2
```

### What happens

For each venue id provided to `search`, the script prints the resolved configuration (venue/day/date/time) and the two URLs, then opens:

1. Group booking search (availability)
2. Booking schedule (existing bookings)

### Output-only mode

Pass `--no-open` to print the URLs without opening any browser tabs:

```bash
reboks search 8 --date '28 Mar' --from '8 AM' --to '3 PM' --no-open
```

### Open only one page

```bash
reboks search 8 --date '28 Mar' --from '8 AM' --to '3 PM' --booking-only
reboks search 8 --date '28 Mar' --from '8 AM' --to '3 PM' --schedule-only
```

## Using the `Config` API directly

You can build your own configs in a Python REPL or script:

```python
from config import Config

c = (
    Config(8)
    .set_day(2)                             # Monday=1 ... Saturday=6
    .set_date("28 Mar 2026", "30 Mar 2026") # date_from, date_to
    .set_time("08:00 AM", "03:00 PM")
)

print(c)
c.open_booking()
c.open_schedule()
```

## Notes

- Dates and times are URL-encoded internally.
- `set_day()` with no argument removes the day filter (search across all days).
- `--date` is a shorthand for setting both `--date-from` and `--date-to` to the same value; it cannot be combined with `--date-from`/`--date-to`.

## Disclaimer

This project is not affiliated with NUS/REBOKS. It simply generates and opens URLs in your browser.
