# Project Documentation

## API

The `repodoc` project provides a CLI tool to generate documentation from Git repositories using Ollama. The following sections describe the project's structure, dependencies, configuration, and usage.

### Project Structure

```text

repodoc/
├── src/
│   └── repodoc/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── chunker.py
│       ├── errors.py
│       ├── generators/
│       │   ├── __init__.py
│       │   ├── api.py
│       │   ├── architecture.py
│       │   ├── base.py
│       │   └── manual.py
│       ├── ollama.py
│       ├── writer.py
├── tests/
│   ├── __init__.py
│   ├── test_chunker.py
│   ├── test_errors.py
│   ├── test_ollama.py
│   ├── generators/
│   │   ├── test_api.py
│   │   ├── test_architecture.py
│   │   └── test_base.py
│   ├── e2e/
│   │   └── test_full_flow.py
├── .gitignore
├── README.md
└── pyproject.toml

```

### Dependencies

The project uses the following dependencies:

- `httpx>=0.28.1`: For making HTTP requests.
- `lxml>=5.1.0`: For parsing XML and HTML documents.
- `rich>=14.0.0`: For rich text output in the terminal.
- `tomli>=2.2.1`: For parsing TOML files.
- `typer>=0.15.4`: For creating CLI applications.

The project also uses the following optional dependencies for development:

- `respx>=0.22.0`: For mocking HTTP requests in tests.
- `black>=24.1.1`: For code formatting.
- `coverage>=7.4.1`: For measuring code coverage.
- `mypy>=1.8.0`: For static type checking.
- `pytest>=8.0.0`: For running tests.
- `pytest-asyncio>=0.23.5`: For running asyncio-based tests.
- `pytest-cov>=4.1.0`: For measuring test coverage.
- `ruff>=0.2.1`: For linting and formatting code.

### Configuration

The project uses the following configuration tools:

- `hatchling`: For building the project.
- `ruff`: For linting and formatting code.
- `pytest`: For running tests.
- `coverage`: For measuring code coverage.
- `mypy`: For static type checking.

### Usage

To use the `repodoc` tool, run the following command:

```bash
repodoc generate --input <path_to_repomix_file> --output <path_to_output_directory> --api --manual
```

The `--input` flag specifies the path to the repomix file. The `--output` flag specifies the path to the output directory where the generated documentation will be saved. The `--api` and `--manual` flags specify which types of documentation to generate.

### Example

Here's an example of how to use the `repodoc` tool:

```bash
repodoc generate --input tests/fixtures/sample.repomix --output out --api --manual
```

This command will generate API and manual documentation for the repomix file at `tests/fixtures/sample.repomix` and save it in the `out` directory.
