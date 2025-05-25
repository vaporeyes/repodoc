"""User manual documentation generator."""

from repodoc.generators.base import DocGenerator, register
from repodoc.ollama import OllamaClient


def build_prompt(project: str) -> str:
    """Build a prompt for user manual generation.

    Args:
        project: Project content to document.

    Returns:
        Prompt string focusing on usage patterns and workflows.
    """
    return f"""Please analyze the following code and generate a user manual in markdown format.
Focus on:
- Getting started guide
- Common usage patterns and workflows
- Step-by-step instructions for key features
- Best practices and tips
- Troubleshooting common issues

Code to analyze:
{project}

Please format the documentation with markdown headers, code blocks, and lists as appropriate.
Start with a level 2 header '## User Manual' and include a '### Getting Started' section."""


@register("manual")
class ManualGenerator(DocGenerator):
    """Generator for user manual documentation.

    This generator creates documentation focused on usage patterns,
    getting started guides, and common workflows.
    """

    async def generate(self, project: str, client: OllamaClient) -> str:
        """Generate user manual documentation.

        Args:
            project: Project content to document.
            client: Ollama client for text generation.

        Returns:
            Generated user manual in markdown format.
        """
        prompt = build_prompt(project)
        return await client.generate(prompt) 