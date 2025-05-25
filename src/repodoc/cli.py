"""Command-line interface for repodoc."""

from typing import NoReturn

import typer

from repodoc import __version__

app = typer.Typer()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def callback(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Generate documentation from repository metadata."""
    pass


@app.command()
def generate() -> NoReturn:
    """Generate documentation."""
    typer.echo("TODO")
    raise typer.Exit(1) 