## User Manual

This document provides a comprehensive guide to using `repodoc`, a tool that generates documentation from Git repositories using Ollama.

### Getting Started

To get started with `repodoc`, follow these steps:

1. **Installation**:
   Ensure you have Python 3.11 or later installed on your system.
   Install `repodoc` using pip:

   ```bash
   pip install repodoc
   ```

2. **Basic Usage**:
   Run the following command to generate documentation from a repository:

   ```bash
   repodoc generate --input /path/to/repository --output /path/to/output/directory --api --manual --architecture
   ```

   Replace `/path/to/repository` with the path to your Git repository and `/path/to/output/directory` with the desired output directory.

### Command-Line Interface

The `repodoc` CLI provides several options for customizing the documentation generation process. Below are the available commands and options:

#### Commands

- **generate**: Generates documentation from a specified input file or directory.

#### Options

- `--input PATH`: Specify the path to the input repository.
- `--output PATH`: Specify the path to the output directory where the generated documentation will be saved.
- `--api`: Generate API documentation.
- `--manual`: Generate user manual.
- `--architecture`: Generate architecture overview.
- `-v, --verbose`: Enable verbose mode for detailed logging.

### Configuration File

`repodoc` uses a configuration file to manage settings. Create a `config.toml` file in the project root with the following content:

```toml
[ollama]
url = "http://localhost:8000"
model = "default"
```

Modify the URL and model as needed.

### Error Handling

`repodoc` provides standardized exit codes for error handling. Below is a list of possible errors and their corresponding codes:

- **General Error**: Exit code `1`
  - Description: Unexpected runtime error.
- **Configuration Error**: Exit code `2`
  - Description: Issues with the configuration file or flags.
- **Input File Error**: Exit code `3`
  - Description: Missing or invalid input file.
- **Ollama Error**: Exit code `4`
  - Description: Cannot reach Ollama server or bad model.
- **Output Directory Error**: Exit code `5`
  - Description: Unable to create or write output directory.

### Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For any issues or questions, please open an issue on GitHub or contact us at <john.smith@example.com>.
