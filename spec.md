# Repomix Documentation Generator - Technical Specification

## Overview

A command-line tool that processes repomix-generated files using local Ollama LLMs to automatically generate different types of documentation in Markdown format.

## Core Functionality

### Supported Documentation Types
- **API Documentation** (`--api`): Generate comprehensive API reference documentation
- **User Manuals** (`--manual`): Generate end-user documentation and guides  
- **Architectural Overviews** (`--architecture`): Generate high-level system architecture documentation

### Output Format
- All documentation generated in Markdown format
- Each documentation type uses tailored prompts and content processing specific to its purpose

## Command Line Interface

### Basic Usage
```bash
tool --input=<repomix-file> --output=<output-directory> [documentation-flags] [options]
```

### Required Parameters
- `--input=<file>`: Path to the repomix-generated file
- `--output=<directory>`: Output directory for generated documentation

### Documentation Type Flags (at least one required)
- `--api`: Generate API documentation
- `--manual`: Generate user manual
- `--architecture`: Generate architectural overview
- Multiple flags can be specified to generate multiple documentation types

### Ollama Configuration Parameters
- `--ollama-url=<url>`: Ollama server URL (default: configuration file or built-in default)
- `--model=<model-name>`: LLM model name (default: configuration file or built-in default)

### Additional Options
- `--verbose`: Enable verbose output showing detailed processing steps
- `--help`: Display usage information and available options

### Example Commands
```bash
# Generate all documentation types
tool --input=repo.txt --output=docs/ --api --manual --architecture

# Generate only API docs with custom Ollama settings
tool --input=repo.txt --output=docs/ --api --ollama-url=http://localhost:11434 --model=codestral

# Generate multiple types with verbose output
tool --input=repo.txt --output=docs/ --api --manual --verbose
```

## Configuration File

### Format and Location
- **File format**: TOML
- **File name**: `config.toml`
- **Location**: Current working directory
- **Precedence**: CLI arguments override configuration file values

### Configuration Structure
```toml
[ollama]
url = "http://localhost:11434"
model = "codestral"
```

### Configuration Parameters
- `ollama.url`: Default Ollama server URL
- `ollama.model`: Default LLM model name

## Output Files

### File Naming Convention
Generated files are placed in the specified output directory with these names:
- `api-docs.md`: API documentation
- `user-manual.md`: User manual documentation  
- `architecture.md`: Architectural overview documentation

### File Generation
- Only requested documentation types are generated
- Each documentation type processes the repomix content differently based on its specific requirements
- Files are created in the specified output directory

## Error Handling Strategy

### Fail-Fast Scenarios (immediate exit)
- Missing or invalid input file
- Unreachable Ollama server
- Invalid configuration file format
- Unable to create output directory
- Missing required parameters

### Continue-on-Error Scenarios
- Individual documentation generation failures
- When generating multiple documentation types, failure of one type doesn't prevent others from being generated
- Clear summary provided at completion showing successes and failures

### Error Messages
- All errors provide clear, helpful messages explaining the issue and potential solutions
- Error messages are user-friendly and actionable

## Progress and Logging

### Progress Indicators
- Always show progress indicators during documentation generation
- Indicate which documentation type is currently being processed
- Show completion status for each documentation type

### Verbose Mode
- Enabled with `--verbose` flag
- Shows detailed processing steps
- Provides additional debugging information
- Displays LLM interaction details

## Content Processing Strategy

### Repomix File Handling
- Parse and validate repomix file format
- Extract codebase content for processing

### Documentation-Specific Processing
Each documentation type uses different content analysis strategies:

- **API Documentation**: Focus on public interfaces, function signatures, endpoints, data structures
- **User Manual**: Emphasize usage patterns, examples, getting started guides, common workflows
- **Architectural Overview**: Highlight system structure, component relationships, design patterns, data flow

### Large File Handling
- Monitor token limits for the specified LLM model
- Provide warning when repomix file may exceed token limits
- Let user handle chunking or file size reduction manually
- Continue processing if user chooses to proceed

## Behavior Specifications

### No Documentation Flags Specified
- Display help message with usage examples
- Exit with status code indicating user input required
- Do not attempt to generate any documentation

### Missing Dependencies
- Check for Ollama server availability at startup
- Validate model availability before processing
- Provide clear error messages for missing dependencies

## Future Extensibility

### Web Interface Support
- CLI architecture should support future web interface implementation
- Core logic should be separable from CLI interface
- Configuration system should be reusable across interfaces

### Additional Documentation Types
- Architecture should support adding new documentation types
- Plugin or module system consideration for future expansion

## Technical Requirements

### Dependencies
- Ollama client library for LLM communication
- TOML parsing library for configuration
- File system operations for input/output handling
- Progress indication library for user feedback

### Error Codes
- 0: Success
- 1: General error
- 2: Configuration error  
- 3: Input file error
- 4: Ollama connection error
- 5: Output directory error

### Performance Considerations
- Asynchronous processing where possible
- Efficient memory usage for large repomix files
- Timeout handling for LLM requests
- Graceful handling of slow LLM responses

Below is a **three-pass plan-refinement** followed by a **library of code-generation prompts**.
Each prompt is wrapped in a `text code-block` so you can copy-paste straight into your favorite LLM (e.g. Codestral, GPT-4o) without further editing.