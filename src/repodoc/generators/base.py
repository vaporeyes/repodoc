"""Base interface for documentation generators."""

from abc import ABC, abstractmethod
from typing import Dict, Type

from repodoc.ollama import OllamaClient


class DocGenerator(ABC):
    """Abstract base class for documentation generators.

    This class defines the interface that all concrete documentation generators
    must implement. The strategy pattern allows for different documentation
    generation approaches to be used interchangeably.
    """

    @abstractmethod
    async def generate(self, project: str, client: OllamaClient) -> str:
        """Generate documentation for a project.

        Args:
            project: Project content to document.
            client: Ollama client for text generation.

        Returns:
            Generated documentation as a string.
        """
        pass


# Registry for concrete generator implementations
_registry: Dict[str, Type[DocGenerator]] = {}


def register(name: str) -> Type[DocGenerator]:
    """Register a concrete generator implementation.

    Args:
        name: Unique identifier for the generator.

    Returns:
        Decorator function that registers the generator class.

    Raises:
        ValueError: If a generator with the given name is already registered.
    """
    def decorator(cls: Type[DocGenerator]) -> Type[DocGenerator]:
        if name in _registry:
            raise ValueError(f"Generator '{name}' is already registered")
        _registry[name] = cls
        return cls
    return decorator


def get_generator(name: str) -> Type[DocGenerator]:
    """Get a registered generator by name.

    Args:
        name: Name of the generator to retrieve.

    Returns:
        The registered generator class.

    Raises:
        KeyError: If no generator is registered with the given name.
    """
    if name not in _registry:
        raise KeyError(f"No generator registered with name '{name}'")
    return _registry[name] 