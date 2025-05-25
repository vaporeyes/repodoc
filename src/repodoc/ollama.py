"""Async client for Ollama API."""

from __future__ import annotations

import json
import httpx
from typing import Optional

from repodoc.errors import OllamaError


class OllamaClient:
    """Client for interacting with Ollama API.

    Attributes:
        url: Base URL for Ollama API.
        model: Name of the model to use.
        client: HTTP client for making requests.
    """

    def __init__(
        self, url: str = "http://localhost:11434", model: str = "devstral"
    ) -> None:
        """Initialize the client.

        Args:
            url: Base URL for Ollama API (e.g., "http://localhost:11434").
            model: Name of the model to use (e.g., "devstral").
        """
        self.base_url = url.rstrip("/")
        self.model = model
        self._client = httpx.AsyncClient(timeout=2.0)  # 2 second timeout

    async def healthcheck(self) -> bool:
        """Check if Ollama server is healthy.

        Returns:
            bool: True if server is healthy.

        Raises:
            OllamaError: If health check fails.
        """
        try:
            response = await self._client.get(self.base_url)
            response.raise_for_status()
            return response.text.strip() == "Ollama is running"
        except httpx.TimeoutException:
            raise OllamaError("Health check timed out")
        except httpx.RequestError as e:
            raise OllamaError(f"Failed to connect to Ollama: {str(e)}")

    async def generate(self, prompt: str, *, temperature: float = 0.2) -> str:
        """Generate text using the Ollama model.

        Args:
            prompt: The prompt to generate text from.
            temperature: Sampling temperature (0.0 to 1.0). Defaults to 0.2.

        Returns:
            Generated text.

        Raises:
            OllamaError: If generation fails.
        """
        try:
            json_data = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
            }
            headers = {
                "Content-Type": "application/json",
            }

            response = await self._client.post(
                f"{self.base_url}/api/generate",
                headers=headers,
                json=json_data,
                timeout=30.0,  # 30 second timeout for generation
            )
            response.raise_for_status()
            
            # Ollama returns a stream of JSON objects, one per line
            full_response = ""
            async for line in response.aiter_lines():
                if line.strip():
                    try:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            full_response += chunk["response"]
                    except json.JSONDecodeError as e:
                        raise OllamaError(f"Failed to parse Ollama response: {e}")
            
            return full_response
        except httpx.TimeoutException:
            raise OllamaError("Generation timed out")
        except httpx.RequestError as e:
            raise OllamaError(f"Failed to generate text: {str(e)}")

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
