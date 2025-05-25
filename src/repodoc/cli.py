"""Command-line interface for repodoc."""

import asyncio
import logging
from pathlib import Path

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm

from repodoc.errors import OutputDirectoryError
from repodoc.generators.base import get_generator
from repodoc.logging import setup_logging
from repodoc.ollama import OllamaClient
from repodoc.parser import run_repomix
from repodoc.writer import write


app = typer.Typer(
    name="repodoc",
    help="Generate documentation from Git repositories using Ollama.",
)


async def _generate_docs(
    repo_path: Path,
    output_dir: Path,
    verbose: bool,
) -> None:
    """Generate documentation from Git repositories using Ollama.

    Args:
        repo_path: Path to Git repository to document.
        output_dir: Directory to write documentation to.
        verbose: Whether to enable verbose logging.
    """
    # Set up logging
    console = setup_logging(verbose)
    logger = logging.getLogger("repodoc")

    try:
        # Run repomix to get project content
        logger.info("Running repomix to analyze repository...")
        project_file = run_repomix(repo_path)
        logger.debug(f"Repomix output: {project_file}")

        # Initialize Ollama client
        logger.info("Initializing Ollama client...")
        client = OllamaClient()
        logger.debug("Ollama client initialized")

        # Generate documentation for each type
        generators = {
            "api": "API documentation",
            "manual": "User manual",
            "architecture": "Architecture documentation",
        }

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            for kind, description in generators.items():
                task = progress.add_task(f"Generating {description}...", total=None)
                
                try:
                    # Get generator and generate documentation
                    generator = get_generator(kind)()
                    doc = await generator.generate(project_file.read_text(), client)
                    
                    # Write documentation to file
                    out_file = write(doc, kind, output_dir)
                    logger.info(f"Wrote {description} to {out_file}")
                    
                except Exception as e:
                    logger.error(f"Failed to generate {description}: {e}")
                    if not Confirm.ask("Continue with remaining documentation?"):
                        raise typer.Exit(1)
                
                progress.update(task, completed=True)

        logger.info("Documentation generation complete!")

    except OutputDirectoryError as e:
        logger.error(f"Output directory error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise typer.Exit(1)
    finally:
        await client.close()


@app.command(name="generate")
def generate(
    repo_path: Path = typer.Argument(
        ...,
        help="Path to Git repository to document.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    output_dir: Path = typer.Option(
        "docs",
        "--output-dir",
        "-o",
        help="Directory to write documentation to.",
        file_okay=False,
        dir_okay=True,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging.",
    ),
) -> None:
    """Generate documentation from Git repositories using Ollama."""
    asyncio.run(_generate_docs(repo_path, output_dir, verbose))


if __name__ == "__main__":
    app() 