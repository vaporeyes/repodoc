"""Error hierarchy and standardized exit codes."""

from enum import IntEnum
from typing import Optional


class ExitCode(IntEnum):
    """Standardized exit codes for the application.

    Attributes:
        SUCCESS: Normal termination.
        GENERAL: Unexpected runtime error.
        CONFIG: Configuration file or flag issues.
        INPUT_FILE: Missing or invalid input file.
        OLLAMA: Cannot reach Ollama server or bad model.
        OUTPUT_DIR: Unable to create or write output directory.
    """

    SUCCESS = 0  # normal termination
    GENERAL = 1  # unexpected runtime error
    CONFIG = 2  # configuration file / flag issues
    INPUT_FILE = 3  # missing or invalid --input file
    OLLAMA = 4  # cannot reach Ollama server / bad model
    OUTPUT_DIR = 5  # unable to create / write output dir


class RepoDocError(Exception):
    """Base class for all repodoc errors.

    Attributes:
        exit_code: The standardized exit code for this error.
        message: Optional error message.
    """

    def __init__(self, exit_code: ExitCode, message: Optional[str] = None) -> None:
        """Initialize the error.

        Args:
            exit_code: The standardized exit code.
            message: Optional error message.
        """
        self.exit_code = exit_code
        super().__init__(message or self.__class__.__name__)


class ConfigurationError(RepoDocError):
    """Configuration file or flag issues."""

    def __init__(self, message: Optional[str] = None) -> None:
        """Initialize the error.

        Args:
            message: Optional error message.
        """
        super().__init__(ExitCode.CONFIG, message)


class InputFileError(RepoDocError):
    """Missing or invalid input file."""

    def __init__(self, message: Optional[str] = None) -> None:
        """Initialize the error.

        Args:
            message: Optional error message.
        """
        super().__init__(ExitCode.INPUT_FILE, message)


class OllamaError(RepoDocError):
    """Cannot reach Ollama server or bad model."""

    def __init__(self, message: Optional[str] = None) -> None:
        """Initialize the error.

        Args:
            message: Optional error message.
        """
        super().__init__(ExitCode.OLLAMA, message)


class OutputDirectoryError(RepoDocError):
    """Unable to create or write output directory."""

    def __init__(self, message: Optional[str] = None) -> None:
        """Initialize the error.

        Args:
            message: Optional error message.
        """
        super().__init__(ExitCode.OUTPUT_DIR, message) 