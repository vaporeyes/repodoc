## 1 · High-Level Blueprint (Pass #1)

| Phase                   | Goal                                     | Key Deliverables                                                       |
| ----------------------- | ---------------------------------------- | ---------------------------------------------------------------------- |
| 0. Project Bootstrap    | Clean repo, automated tooling            | **pyproject.toml**, `src/repodoc/__init__.py`, pre-commit, CI skeleton |
| 1. CLI Skeleton         | Argument parsing & exit codes            | Typer CLI + `--help/--version`                                         |
| 2. Config Handling      | TOML config + override rules             | `config.py`, unit tests                                                |
| 3. Repomix Parser       | Read + validate repomix format           | `parser.py`, sample fixtures                                           |
| 4. Ollama Client        | Thin async wrapper + health-check        | `ollama.py`, mock tests                                                |
| 5. Doc Generators       | Strategy pattern for API, Manual, Arch   | `generators/*.py`, common base                                         |
| 6. Output Writer        | Markdown emit + filename rules           | `writer.py`, integration tests                                         |
| 7. Progress / Verbose   | Rich progress bar + verbose logs         | `progress.py`, CLI flag wiring                                         |
| 8. Error Handling       | Fail-fast vs continue-on                 | `errors.py`, exhaustive unit tests                                     |
| 9. End-to-End Flow      | Real-world scenario test                 | `tests/e2e/test_full_flow.py`                                          |
| 10. Packaging & Release | Build wheels, make-release GitHub Action | `RELEASE.md`, tagged version                                           |

---

## 2 · First Breakdown into Iterative Chunks (Pass #2)

1. **Scaffolding & CI**
2. **CLI Baseline**
3. **Config Loader**
4. **Repomix Parser (read-only)**
5. **Error Types & Codes**
6. **Ollama Client Stub**
7. **Generator Interface**
8. **API Doc Generator Impl**
9. **Manual Generator Impl**
10. **Architecture Generator Impl**
11. **Writer & File System logic**
12. **Progress / Verbose wiring**
13. **End-to-End happy-path**
14. **Failure Path tests**
15. **Packaging & Release automation**

---

## 3 · Second Breakdown: Right-Sized Steps (Pass #3)

| Chunk | Step | Description                                                      | Size Check |
| ----- | ---- | ---------------------------------------------------------------- | ---------- |
| 1     | 1.1  | Create **pyproject**, set Python ≥ 3.12, add Typer, pytest, rich | ✅ Small    |
|       | 1.2  | Init **src/repodoc/** with `__init__.py` exposing `__version__`  | ✅          |
|       | 1.3  | Add **pre-commit** with black, ruff, mypy                        | ✅          |
|       | 1.4  | Add **GitHub Action** running tests & lint                       | ✅          |
| 2     | 2.1  | Implement Typer app with `--help/--version` only                 | ✅          |
|       | 2.2  | Add exit-code enum in `errors.py`                                | ✅          |
|       | 2.3  | Unit-test CLI invocation via Typer’s CliRunner                   | ✅          |
| 3     | 3.1  | Implement `config.load(path=None)` returning dataclass           | ✅          |
|       | 3.2  | Override logic (CLI > env > file > defaults)                     | ✅          |
|       | 3.3  | Tests covering precedence matrix                                 | ✅          |
| 4     | 4.1  | Define repomix file mimimum viable schema (YAML/TOML?)           | ✅          |
|       | 4.2  | Implement `parser.parse(path)` returning `ProjectModel`          | ✅          |
|       | 4.3  | Unit tests with fixtures (valid + invalid)                       | ✅          |
| 5     | 5.1  | Enumerate `ExitCode` constants (0-5)                             | ✅          |
|       | 5.2  | Raise custom `RepodocError` subclasses                           | ✅          |
| 6     | 6.1  | Implement `OllamaClient.healthcheck()` with timeout              | ✅          |
|       | 6.2  | Implement `OllamaClient.generate(prompt, *, model)` stub         | ✅          |
|       | 6.3  | Mock tests (no live network)                                     | ✅          |
| 7     | 7.1  | Abstract base `DocGenerator` with `generate(project)`            | ✅          |
|       | 7.2  | Registry mapping flag → concrete class                           | ✅          |
| 8     | 8.1  | Implement `ApiGenerator` (prompts only)                          | ✅          |
|       | 8.2  | Snapshot tests on prompt formation                               | ✅          |
| 9     | 9.1  | Implement `ManualGenerator`                                      | ✅          |
| 10    | 10.1 | Implement `ArchitectureGenerator`                                | ✅          |
| 11    | 11.1 | Implement `writer.write(doc, kind, out_dir)`                     | ✅          |
|       | 11.2 | Tests for directory creation, overwrite rules                    | ✅          |
| 12    | 12.1 | Add Rich progress bar, wire into CLI                             | ✅          |
|       | 12.2 | Add `--verbose` flag toggling log level                          | ✅          |
| 13    | 13.1 | Happy-path end-to-end test using tempfs & mocked Ollama          | ✅          |
| 14    | 14.1 | Failure when Ollama offline → exit-code 4                        | ✅          |
|       | 14.2 | Failure when input missing → exit-code 3                         | ✅          |
| 15    | 15.1 | `task release` script builds wheel & twine upload (dry run)      | ✅          |
|       | 15.2 | Update README with usage examples                                | ✅          |

*Each step fits in ≤ 150 LOC (implementation + tests) and introduces one concept only — small enough for TDD, large enough to progress.*

---

## 4 · Code-Generation Prompts Library

> **Usage**: Feed each prompt to your code-generation LLM sequentially.
> Replace `{{STEPNO}}` with the actual step number if desired.

### Prompt 1.1 – Project Bootstrap

```text
You are writing Step 1.1 of Repomix Documentation Generator.

**Goal**: Create project scaffolding.

1. Generate a *pyproject.toml* using PEP 621 metadata:
   - project name: repodoc
   - version: 0.0.1
   - dependencies: typer>=0.12, rich>=13.7, tomli>=2.0, httpx>=0.27
   - optional-dev dependencies group "dev": pytest>=8.2, pytest-cov, black, ruff, mypy, pre-commit

2. Create directory structure:
```

src/
repodoc/
**init**.py    # defines **version**

```

3. Configure *pre-commit* with hooks: ruff-format, black, ruff-lint, mypy, pytest.

4. Output **NO additional code** besides these files.

5. Provide *pytest* stub that asserts `repodoc.__version__ == "0.0.1"`.

Return the full file contents ready to commit. Use best practices and keep it minimal.
```

---

### Prompt 1.2 – GitHub CI

```text
Step 1.2 – Add GitHub Action.

Create *.github/workflows/ci.yml* that:

- Runs on push & PR to main
- Matrix over Python 3.12 and 3.13
- Caches pip
- Installs dev deps via `pip install -e .[dev]`
- Runs `ruff format --check`, `ruff check`, `black --check .`, `mypy src`, and `pytest -q --cov=repodoc`

Return the YAML only.
```

---

### Prompt 2.1 – CLI Baseline

```text
Step 2.1 – Implement the minimal CLI.

1. Inside *src/repodoc/cli.py* create a Typer app named `app`.
2. Add `--version` option that prints `repodoc.__version__` and exits.
3. Add a placeholder command `generate` that currently just echoes `"TODO"` and exits 1.
4. Add an `entry_points` console-script `repodoc=repodoc.cli:app` in *pyproject.toml*.

Write unit tests in *tests/test_cli_baseline.py* using Typer’s CliRunner:

- `repodoc --version` exits 0 and prints 0.0.1
- `repodoc generate` exits 1

No other behaviour yet. Keep functions small, include type hints, be PEP 8 compliant.
```

---

### Prompt 3.1 – Configuration Loader

```text
Step 3.1 – Implement TOML config loader with override precedence.

Specification:
- File *src/repodoc/config.py* exposes `Config` dataclass with:
    - ollama_url: str = "http://localhost:11434"
    - model: str = "codestral"
- Function `load(cli_args: dict[str, str | None]) -> Config`
    1. Load config from `config.toml` if present in cwd.
    2. Environment vars `REPODOC_OLLAMA_URL`, `REPODOC_MODEL` override file.
    3. Finally, CLI args override env/file.
- Validation: ensure URL starts with http:// or https:// else raise `ConfigurationError`.
- Unit tests cover all precedence combinations.

Provide updated code & tests only.
```

---

Step 4.1 – Implement FileChunker.

Goal  
Read any text file (the repomix XML) and yield “prompt-sized” chunks that keep each chunk under
`max_tokens` (default: 16 000) using a 4-chars≈1-token heuristic.

Files  
*src/repodoc/chunker.py*

```python
from pathlib import Path
from typing import Iterable, Iterator

def iter_chunks(path: Path, *, max_tokens: int = 16_000) -> Iterator[str]:
    max_chars = max_tokens * 4
    buf: list[str] = []
    length = 0
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            buf.append(line)
            length += len(line)
            if length >= max_chars:
                yield "".join(buf)
                buf.clear()
                length = 0
    if buf:
        yield "".join(buf)
...
```

---

Step 5.1 – Define error hierarchy and standardized exit codes.

Context  

* Steps 1-4 are done (CLI baseline, config loader WIP).  
* We need a single place for every fail-fast / continue-on error to live.

Tasks

1. **Create *src/repodoc/errors.py***  

   ```python
   from enum import IntEnum

   class ExitCode(IntEnum):
       SUCCESS = 0          # normal termination
       GENERAL = 1          # unexpected runtime error
       CONFIG = 2           # configuration file / flag issues
       INPUT_FILE = 3       # missing or invalid --input file
       OLLAMA = 4           # cannot reach Ollama server / bad model
       OUTPUT_DIR = 5       # unable to create / write output dir


---

### Prompt 6.1 – Ollama Client Stub

```text
Step 6.1 – Implement async Ollama client stub.

Files:
- *src/repodoc/ollama.py*
   * Define `class OllamaClient` with:
       - `__init__(url: str, model: str)`
       - async `healthcheck()` -> bool (GET /api/health, handle timeout 2s)
       - async `generate(prompt: str, *, temperature: float = 0.2) -> str`
         (for now: raise NotImplementedError)
- *tests/test_ollama.py* using respx to mock httpx responses:
   - healthcheck success returns True
   - timeout returns False

Do not add CLI hooks yet.
```

---

### Prompt 7.1 – Generator Interface

```text
Step 7.1 – Strategy pattern for documentation generators.

1. *src/repodoc/generators/base.py*
   - `class DocGenerator(ABC)` with abstract `generate(project, client) -> str`
   - `registry: dict[str, type[DocGenerator]]`
   - Decorator `@register(name)` to add concrete class.

2. Example concrete stub `ApiGenerator` in *src/repodoc/generators/api.py* that builds an English prompt (no Ollama call yet) and returns `"API DOC\n"`.

3. Tests:
   - `registry["api"] is ApiGenerator`
   - `ApiGenerator().generate(...)` returns string.

Focus on architecture, not content.
```

---

### Step 8.1 – Implement ApiGenerator

Context: `DocGenerator` base/registry already exist.

Tasks

1. In *src/repodoc/generators/api.py*
   * Subclass `DocGenerator`.
   * `generate(project, client)` should:
        a. Build an English prompt focusing on public interfaces, function signatures, and data structures contained in `project`.
        b. Call `await client.generate(prompt)` (for now streak to sync version with `asyncio.run()` if needed).
        c. Return the markdown string from Ollama unchanged.
2. Add helper `build_prompt(project)` pure-function for unit-testing.
3. Tests in *tests/generators/test_api.py*
   * Patch `OllamaClient.generate` to return `"## API\nContent"`.
   * Assert returned doc starts with `## API`.

---

### Step 8.2 – Implement ManualGenerator

1. *src/repodoc/generators/manual.py*
   * Focus on usage patterns, getting-started, common workflows.
2. Re-use template helper similar to ApiGenerator.
3. Snapshot tests ensuring prompt contains the phrase “Step-by-step guide”.

---

### Step 8.3 – Implement ArchitectureGenerator

1. *src/repodoc/generators/architecture.py*
   * Produce a prompt that asks the LLM for a high-level overview plus Mermaid sequence/flow diagrams.
2. When returned markdown contains triple-back-tick `mermaid`, leave as-is.
3. Tests ensure at least one “```mermaid” block exists in output.

---

### Step 9.1 – Write markdown files safely

Create *src/repodoc/writer.py* exposing `write(doc: str, kind: str, out_dir: Path) -> Path` that:

* Ensures `out_dir` exists (`mkdir(parents=True, exist_ok=True)`).
* Maps `kind` → filename: `api`→api-docs.md, `manual`→user-manual.md, `architecture`→architecture.md.
* Writes UTF-8, newline `\n`, returns Path.
* If file exists, overwrite atomically (tmp-file + rename).
* Raises `OutputDirError` if dir cannot be created or is not writable.

Tests using `tmp_path` verify file creation and overwrite.

---

### Step 10.1 – Wire progress indicator & verbose logging

Requirements

1. Add global `--verbose / -v` option in Typer that sets log level DEBUG; default INFO.
2. Introduce `rich.console.Console` + `logging` RichHandler.
3. Implement `rich.progress.Progress` in CLI `generate` loop:

---

### Prompt 11.1 – Writer & File System

```text
Step 11.1 – Write markdown files safely.

Create *src/repodoc/writer.py* exposing `write(doc: str, kind: str, out_dir: Path) -> Path` that:

- Ensures `out_dir` exists (`mkdir(parents=True, exist_ok=True)`).
- Maps `kind` → filename: `api`→api-docs.md, `manual`→user-manual.md, `architecture`→architecture.md.
- Writes UTF-8, newline `\n`, and returns Path.
- If file exists, overwrite.
- Raises `OutputDirError` if cannot create dir.

Tests using tempfile ensure file is written and re-written.
```

---

### Prompt 12.1 – Progress & Verbose

```text
Step 12.1 – Wire progress indicator & verbose logging.

Requirements:
1. Add `--verbose / -v` global Typer option setting log level to DEBUG, else INFO. Use `logging` + `rich.console.Console` for colour.
2. Add `Progress` object from `rich.progress` to wrap generator loop:
```

for kind, gen\_cls in selected\_generators:
task = progress.add\_task(kind, total=None)
...
progress.update(task, advance=1, description=f"{kind} done")

```
3. Update CLI `generate` command to:
- Validate input file & flags
- Load config
- Health-check Ollama
- Parse repomix
- Iterate generators → writer
- Exit correct codes on failure

Write integration test with mocked Ollama returning True.

Keep diff small: modify only cli.py and add progress.py helper if useful.
```

---

### Prompt 13.1 – End-to-End Happy Path

```text
Step 13.1 – End-to-end test.

In *tests/e2e/test_full_flow.py*:

- Create temp repomix file with two snippets.
- Create temp output dir.
- Monkeypatch OllamaClient.generate to return "dummy doc".
- Run CLI: `repodoc generate --input tmpfile --output out --api --manual`
- Assert exit code 0 and that *api-docs.md* and *user-manual.md* exist with content.

Use subprocess/runpy or Typer CliRunner as you prefer.
```

---

*(Continue similar prompts for failure paths & release automation as needed.)*

---

### How to Use These Prompts

1. Feed **Prompt 1.1** to your LLM, commit the result.
2. Run `pytest` – it should pass (TDD gate).
3. Proceed with **Prompt 1.2**, commit, green tests again.
4. Continue sequentially. Each prompt assumes all previous steps are merged and passing.

Because every prompt ends by updating tests, the code base is continuously integrated and no orphan code remains. At the end you’ll have a fully wired tool with strong coverage and a clear release path.

Happy building!
