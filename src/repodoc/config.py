"""Configuration management for repodoc."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import tomli

from repodoc.errors import ConfigurationError


@dataclass
class Config:
    """Configuration for repodoc."""

    ollama_url: str = "http://localhost:11434"
    model: str = "codestral"


def load(cli_args: dict[str, Optional[str]] = None) -> Config:
    """Load configuration with override precedence.

    Args:
        cli_args: Optional CLI arguments to override config.

    Returns:
        Config object with resolved values.

    Raises:
        ConfigurationError: If URL is invalid or config file is malformed.
    """
    cli_args = cli_args or {}
    config = Config()

    # 1. Load from config.toml if present
    config_path = Path("config.toml")
    if config_path.exists():
        try:
            with config_path.open("rb") as f:
                data = tomli.load(f)
                if "ollama" in data:
                    if "url" in data["ollama"]:
                        config.ollama_url = data["ollama"]["url"]
                    if "model" in data["ollama"]:
                        config.model = data["ollama"]["model"]
        except tomli.TOMLDecodeError as e:
            raise ConfigurationError(f"Invalid config.toml: {e}") from e

    # 2. Override with environment variables
    if url := os.environ.get("REPODOC_OLLAMA_URL"):
        config.ollama_url = url
    if model := os.environ.get("REPODOC_MODEL"):
        config.model = model

    # 3. Override with CLI arguments
    if url := cli_args.get("ollama_url"):
        config.ollama_url = url
    if model := cli_args.get("model"):
        config.model = model

    # Validate URL
    if not config.ollama_url.startswith(("http://", "https://")):
        raise ConfigurationError(
            f"Invalid Ollama URL: {config.ollama_url}. Must start with http:// or https://"
        )

    return config 