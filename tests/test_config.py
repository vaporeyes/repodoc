"""Tests for configuration management."""

import os
from pathlib import Path
from typing import Optional

import pytest
import tomli

from repodoc.config import Config, load
from repodoc.errors import ConfigurationError
from conftest import as_cwd


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    """Create a temporary config file.

    Args:
        tmp_path: Pytest fixture providing temporary directory.

    Returns:
        Path to the config file.
    """
    config = tmp_path / "config.toml"
    config.write_text(
        """[ollama]
url = "http://localhost:11434"
model = "codestral"
"""
    )
    return config


def test_default_config() -> None:
    """Test default configuration values."""
    config = load()
    assert config.ollama_url == "http://localhost:11434"
    assert config.model == "codestral"


def test_config_file(config_file: Path) -> None:
    """Test loading from config file.

    Args:
        config_file: Path to config file.
    """
    with as_cwd(config_file.parent):
        config = load()
        assert config.ollama_url == "http://localhost:11434"
        assert config.model == "codestral"


def test_env_override(config_file: Path) -> None:
    """Test environment variable override.

    Args:
        config_file: Path to config file.
    """
    with as_cwd(config_file.parent):
        os.environ["REPODOC_OLLAMA_URL"] = "http://custom:11434"
        os.environ["REPODOC_MODEL"] = "custom-model"
        try:
            config = load()
            assert config.ollama_url == "http://custom:11434"
            assert config.model == "custom-model"
        finally:
            del os.environ["REPODOC_OLLAMA_URL"]
            del os.environ["REPODOC_MODEL"]


def test_cli_override(config_file: Path) -> None:
    """Test CLI argument override.

    Args:
        config_file: Path to config file.
    """
    with as_cwd(config_file.parent):
        os.environ["REPODOC_OLLAMA_URL"] = "http://env:11434"
        os.environ["REPODOC_MODEL"] = "env-model"
        try:
            config = load(
                {
                    "ollama_url": "http://cli:11434",
                    "model": "cli-model",
                }
            )
            assert config.ollama_url == "http://cli:11434"
            assert config.model == "cli-model"
        finally:
            del os.environ["REPODOC_OLLAMA_URL"]
            del os.environ["REPODOC_MODEL"]


def test_invalid_url() -> None:
    """Test invalid URL validation."""
    with pytest.raises(ConfigurationError, match="Invalid Ollama URL"):
        load({"ollama_url": "invalid-url"})


def test_invalid_config_file(tmp_path: Path) -> None:
    """Test invalid config file.

    Args:
        tmp_path: Pytest fixture providing temporary directory.
    """
    config = tmp_path / "config.toml"
    config.write_text("invalid toml content")
    with as_cwd(config.parent):
        with pytest.raises(ConfigurationError, match="Invalid config.toml"):
            load() 