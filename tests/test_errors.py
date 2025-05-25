"""Tests for the error hierarchy."""

import pytest

from repodoc.errors import (
    ConfigurationError,
    ExitCode,
    InputFileError,
    OllamaError,
    OutputDirectoryError,
    RepoDocError,
)


def test_exit_codes() -> None:
    """Test that exit codes are properly defined."""
    assert ExitCode.SUCCESS == 0
    assert ExitCode.GENERAL == 1
    assert ExitCode.CONFIG == 2
    assert ExitCode.INPUT_FILE == 3
    assert ExitCode.OLLAMA == 4
    assert ExitCode.OUTPUT_DIR == 5


def test_base_error() -> None:
    """Test the base error class."""
    error = RepoDocError(ExitCode.GENERAL, "test message")
    assert error.exit_code == ExitCode.GENERAL
    assert str(error) == "test message"

    # Test default message
    error = RepoDocError(ExitCode.GENERAL)
    assert str(error) == "RepoDocError"


def test_configuration_error() -> None:
    """Test configuration error."""
    error = ConfigurationError("invalid config")
    assert error.exit_code == ExitCode.CONFIG
    assert str(error) == "invalid config"

    # Test default message
    error = ConfigurationError()
    assert str(error) == "ConfigurationError"


def test_input_file_error() -> None:
    """Test input file error."""
    error = InputFileError("file not found")
    assert error.exit_code == ExitCode.INPUT_FILE
    assert str(error) == "file not found"

    # Test default message
    error = InputFileError()
    assert str(error) == "InputFileError"


def test_ollama_error() -> None:
    """Test Ollama error."""
    error = OllamaError("server unreachable")
    assert error.exit_code == ExitCode.OLLAMA
    assert str(error) == "server unreachable"

    # Test default message
    error = OllamaError()
    assert str(error) == "OllamaError"


def test_output_directory_error() -> None:
    """Test output directory error."""
    error = OutputDirectoryError("permission denied")
    assert error.exit_code == ExitCode.OUTPUT_DIR
    assert str(error) == "permission denied"

    # Test default message
    error = OutputDirectoryError()
    assert str(error) == "OutputDirectoryError" 