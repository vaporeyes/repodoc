"""API documentation generator."""

from repodoc.generators.base import DocGenerator, register
from repodoc.ollama import OllamaClient


@register("api")
class ApiGenerator(DocGenerator):
    """Generator for API documentation.

    This generator creates documentation focused on API endpoints, methods,
    parameters, and responses.
    """

    async def generate(self, project: str, client: OllamaClient) -> str:
        """Generate API documentation.

        Args:
            project: Project content to document.
            client: Ollama client for text generation.

        Returns:
            Generated API documentation.
        """
        # TODO: Implement actual documentation generation
        return "API DOC\n" 