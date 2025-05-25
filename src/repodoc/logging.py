"""Logging configuration with Rich integration."""

import logging
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler


def setup_logging(verbose: bool = False) -> Console:
    """Set up logging with Rich integration.

    Args:
        verbose: Whether to enable debug logging.

    Returns:
        Rich console instance.
    """
    # Create console for rich output
    console = Console()

    # Configure logging
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )

    return console 