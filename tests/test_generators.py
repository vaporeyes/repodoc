"""Tests for documentation generators."""

import pytest
from unittest.mock import AsyncMock, patch

from repodoc.generators.base import DocGenerator, get_generator, register
from repodoc.generators.api import ApiGenerator, build_prompt as build_api_prompt
from repodoc.generators.manual import ManualGenerator, build_prompt as build_manual_prompt
from repodoc.ollama import OllamaClient


def test_generator_registry() -> None:
    """Test that generators are properly registered."""
    assert get_generator("api") is ApiGenerator
    assert get_generator("manual") is ManualGenerator


def test_build_api_prompt() -> None:
    """Test API prompt building."""
    project = "def example(): pass"
    prompt = build_api_prompt(project)
    assert "Please analyze the following code" in prompt
    assert "Focus on:" in prompt
    assert "Public interfaces" in prompt
    assert "def example(): pass" in prompt
    assert "Start with a level 2 header '## API'" in prompt


def test_build_manual_prompt() -> None:
    """Test manual prompt building."""
    project = "def example(): pass"
    prompt = build_manual_prompt(project)
    assert "Please analyze the following code" in prompt
    assert "Focus on:" in prompt
    assert "Getting started guide" in prompt
    assert "Step-by-step instructions" in prompt
    assert "def example(): pass" in prompt
    assert "Start with a level 2 header '## User Manual'" in prompt
    assert "### Getting Started" in prompt


@pytest.mark.asyncio
async def test_api_generator() -> None:
    """Test the API generator."""
    generator = ApiGenerator()
    client = OllamaClient()
    
    # Mock the generate method to return a test response
    client.generate = AsyncMock(return_value="## API\nTest content")
    
    result = await generator.generate("test project", client)
    assert result.startswith("## API")
    assert "Test content" in result
    
    # Verify the client was called with the correct prompt
    client.generate.assert_called_once()
    call_args = client.generate.call_args[0][0]
    assert "Please analyze the following code" in call_args
    assert "test project" in call_args


@pytest.mark.asyncio
async def test_manual_generator() -> None:
    """Test the manual generator."""
    generator = ManualGenerator()
    client = OllamaClient()
    
    # Mock the generate method to return a test response
    client.generate = AsyncMock(return_value="## User Manual\n### Getting Started\nStep-by-step guide")
    
    result = await generator.generate("test project", client)
    assert result.startswith("## User Manual")
    assert "### Getting Started" in result
    assert "Step-by-step guide" in result
    
    # Verify the client was called with the correct prompt
    client.generate.assert_called_once()
    call_args = client.generate.call_args[0][0]
    assert "Please analyze the following code" in call_args
    assert "test project" in call_args
    assert "Getting started guide" in call_args


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