"""Error types for repodoc."""

from enum import IntEnum


class ExitCode(IntEnum):
    """Exit codes for the CLI."""

    SUCCESS = 0
    GENERAL_ERROR = 1
    CONFIGURATION_ERROR = 2
    INPUT_FILE_ERROR = 3
    OLLAMA_CONNECTION_ERROR = 4
    OUTPUT_DIR_ERROR = 5


class RepodocError(Exception):
    """Base exception for repodoc."""

    def __init__(self, message: str, exit_code: ExitCode = ExitCode.GENERAL_ERROR) -> None:
        """Initialize error.

        Args:
            message: Error message.
            exit_code: Exit code to use when this error occurs.
        """
        super().__init__(message)
        self.exit_code = exit_code


class ConfigurationError(RepodocError):
    """Configuration-related error."""

    def __init__(self, message: str) -> None:
        """Initialize error.

        Args:
            message: Error message.
        """
        super().__init__(message, ExitCode.CONFIGURATION_ERROR) 