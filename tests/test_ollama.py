"""Tests for the Ollama client."""

import pytest
import respx
from httpx import Response

from repodoc.errors import OllamaError
from repodoc.ollama import OllamaClient


@pytest.fixture
def client() -> OllamaClient:
    """Create an Ollama client for testing.

    Returns:
        OllamaClient instance.
    """
    return OllamaClient()


@pytest.mark.asyncio
async def test_healthcheck_success(client: OllamaClient, respx_mock: respx.MockRouter) -> None:
    """Test successful healthcheck.

    Args:
        client: Ollama client fixture.
        respx_mock: Respx mock router.
    """
    respx_mock.get("http://localhost:11434").mock(
        return_value=Response(200, text="Ollama is running")
    )
    assert await client.healthcheck() is True


@pytest.mark.asyncio
async def test_client_close(client: OllamaClient) -> None:
    """Test client close method.

    Args:
        client: Ollama client fixture.
    """
    await client.close()  # Should not raise any errors 