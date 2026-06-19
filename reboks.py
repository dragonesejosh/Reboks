#!/usr/bin/env python3
"""Main entry point for Reboks command-line application."""

import sys
from argparse import ArgumentParser

from config import Config
from filters import group_venue_filter


def resolve_venue_id(venue_token):
    try:
        return int(venue_token)
    except ValueError as exc:
        raise ValueError(
            f"Unknown venue '{venue_token}'. Use a numeric venue id."
        ) from exc


def parse_date_args(args, parser):
    if args.date and (args.date_from or args.date_to):
        parser.error("--date cannot be used with --date-from or --date-to")

    if args.date:
        return args.date, args.date

    if args.date_from and args.date_to:
        return args.date_from, args.date_to

    parser.error("Provide either --date or both --date-from and --date-to")


def build_base_config(args, parser):
    date_from, date_to = parse_date_args(args, parser)
    if not args.time_from or not args.time_to:
        parser.error("Both --from and --to are required")

    base = Config(1).set_date(date_from, date_to).set_time(args.time_from, args.time_to)
    if args.day is not None:
        base.set_day(args.day)
    return base

def run_list_all_venues(_args):
    print("Venues:")
    if len(_args.venues) == 0:
        for venue_id in sorted(group_venue_filter, key=lambda x: int(x)):
            print(f"  {venue_id:3} -> {group_venue_filter[venue_id]}")
    else:
        for venue_id in _args.venues:
            print(f"  {venue_id:3} -> {group_venue_filter[venue_id]}")

    return 0

def run_search(args, parser):
    base = build_base_config(args, parser)

    for token in args.venues:
        try:
            venue_id = resolve_venue_id(token)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 2

        config = Config(venue_id, base)

        print(config)
        print(f"Booking URL:  {config.booking_url()}")
        print(f"Schedule URL: {config.schedule_url()}")
        print()

        if args.no_open:
            continue

        if not args.schedule_only:
            config.open_booking()
        if not args.booking_only:
            config.open_schedule()

    return 0


def build_parser():
    parser = ArgumentParser(
        prog="reboks",
        description="Build and open NUS REBOKS booking URLs from numeric venue ids.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    list_parser = subparsers.add_parser(
        "list",
        help="List all known venues and their numeric ids.",
    )
    list_parser.set_defaults(handler=run_list_all_venues)
    list_parser.add_argument(
        "venues",
        nargs="*",
        help="Numeric venue ids.",
    )

    search_parser = subparsers.add_parser(
        "search",
        help="Search one or more numeric venue ids.",
        epilog=(
            "Example:"
            "  reboks search 8 2 --date '28 Mar' --from '8 AM' --to '3 PM'\n"
        ),
    )
    search_parser.add_argument(
        "venues",
        nargs="+",
        help="Numeric venue ids.",
    )
    search_parser.add_argument(
        "--date", "-d",
        help="Single date for both from/to, for example '28 Mar'.",
    )
    search_parser.add_argument(
        "--date-from", "-df",
        help="Start date, for example '28 Mar'.",
    )
    search_parser.add_argument(
        "--date-to", "-dt",
        help="End date, for example '29 Mar'.",
    )
    search_parser.add_argument(
        "--from", "-f",
        dest="time_from",
        help="Start time, for example '8 AM'. Required.",
    )
    search_parser.add_argument(
        "--to", "-t",
        dest="time_to",
        help="End time, for example '3 PM'. Required.",
    )
    search_parser.add_argument(
        "--day", "-D",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        help="Day filter, Monday=1 ... Saturday=6. Omit for Any.",
    )
    search_parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open browser tabs. Only print resolved URLs.",
    )

    mode_group = search_parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--booking-only",
        action="store_true",
        help="Open only the group booking page.",
    )
    mode_group.add_argument(
        "--schedule-only",
        action="store_true",
        help="Open only the booking schedule page.",
    )

    search_parser.set_defaults(handler=lambda args: run_search(args, parser))
    return parser


def main():
    """Main entry point for the Reboks CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())