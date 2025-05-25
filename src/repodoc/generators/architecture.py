"""Architecture documentation generator."""

from repodoc.generators.base import DocGenerator, register
from repodoc.ollama import OllamaClient


def build_prompt(project: str) -> str:
    """Build a prompt for architecture documentation generation.

    Args:
        project: Project content to document.

    Returns:
        Prompt string focusing on system architecture and diagrams.
    """
    return f"""Please analyze the following code and generate architecture documentation in markdown format.
Focus on:
- High-level system overview
- Component relationships and interactions
- Data flow and processing pipelines
- Key architectural decisions and patterns

Include Mermaid diagrams for:
- Component sequence diagrams showing key interactions
- Flow diagrams illustrating data movement
- System architecture diagrams showing component relationships

Code to analyze:
{project}

Please format the documentation with markdown headers and code blocks.
Start with a level 2 header '## Architecture'.
Use triple backticks with 'mermaid' for diagrams, like this:
```mermaid
sequenceDiagram
    participant A
    participant B
    A->>B: Hello
```

Ensure at least one Mermaid diagram is included in the documentation."""


@register("architecture")
class ArchitectureGenerator(DocGenerator):
    """Generator for architecture documentation.

    This generator creates documentation focused on system architecture,
    component relationships, and includes Mermaid diagrams for visualization.
    """

    async def generate(self, project: str, client: OllamaClient) -> str:
        """Generate architecture documentation.

        Args:
            project: Project content to document.
            client: Ollama client for text generation.

        Returns:
            Generated architecture documentation in markdown format.
        """
        prompt = build_prompt(project)
        return await client.generate(prompt) 