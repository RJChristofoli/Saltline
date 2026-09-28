"""Command-line entry point for Saltline."""

import argparse
from collections.abc import Sequence
from importlib.metadata import version


def main(argv: Sequence[str] | None = None) -> int:
    """Parse CLI arguments and return a process exit status."""
    parser = argparse.ArgumentParser(
        prog="saltline",
        description="Architecture intelligence for safer software changes.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version('saltline')}",
    )
    parser.parse_args(argv)
    return 0
