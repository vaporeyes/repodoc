"""API documentation generator."""

from repodoc.generators.base import DocGenerator, register
from repodoc.ollama import OllamaClient


def build_prompt(project: str) -> str:
    """Build a prompt for API documentation generation.

    Args:
        project: Project content to document.

    Returns:
        Prompt string focusing on public interfaces and data structures.
    """
    return f"""Please analyze the following code and generate API documentation in markdown format.
Focus on:
- Public interfaces and their signatures
- Function parameters and return types
- Data structures and their fields
- Usage examples where appropriate

Code to analyze:
{project}

Please format the documentation with markdown headers, code blocks, and lists as appropriate.
Start with a level 2 header '## API'."""


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
            Generated API documentation in markdown format.
        """
        prompt = build_prompt(project)
        return await client.generate(prompt) 