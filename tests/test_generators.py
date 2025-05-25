"""Tests for documentation generators."""

import pytest

from repodoc.generators.base import DocGenerator, get_generator, register
from repodoc.generators.api import ApiGenerator
from repodoc.ollama import OllamaClient


def test_generator_registry() -> None:
    """Test that generators are properly registered."""
    assert get_generator("api") is ApiGenerator


@pytest.mark.asyncio
async def test_api_generator() -> None:
    """Test the API generator stub."""
    generator = ApiGenerator()
    client = OllamaClient()
    result = await generator.generate("test project", client)
    assert result == "API DOC\n"


def test_duplicate_registration() -> None:
    """Test that duplicate generator registration is prevented."""
    with pytest.raises(ValueError, match="Generator 'api' is already registered"):

        @register("api")
        class DuplicateGenerator(DocGenerator):
            async def generate(self, project: str, client: OllamaClient) -> str:
                return ""


def test_get_nonexistent_generator() -> None:
    """Test that getting a nonexistent generator raises an error."""
    with pytest.raises(KeyError, match="No generator registered with name 'nonexistent'"):
        get_generator("nonexistent") 