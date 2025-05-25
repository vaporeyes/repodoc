# ✅ Repodoc Documentation Generator — Master TODO

A hierarchical, box-ticking checklist covering **every task** required to deliver the CLI, tests, automation, and release pipeline.  
Use your editor’s markdown-checkbox support (`-[ ]`) or GitHub’s task-list to track progress.

---

## 0 · Workstation & Repo Preparation
- [ ] Install **Python 3.12** (or newer) via pyenv/asdf
- [ ] `python -m venv .venv && source .venv/bin/activate`
- [ ] `pip install --upgrade pip`
- [ ] Create empty Git repo `git init repodoc && cd repodoc`
- [ ] Create **develop** branch from *main*
- [ ] Configure global Git hooks to respect line endings & whitespace
- [ ] Add `.editorconfig` for consistent indentation
- [ ] Configure IDE to use black, ruff, mypy

---

## 1 · Project Bootstrap
### 1.1 Pyproject & Package Skeleton
- [ ] Draft `pyproject.toml` (PEP 621) with minimal metadata
- [ ] Define runtime deps: typer, rich, tomli, httpx
- [ ] Define `[project.optional-dependencies.dev]`
- [ ] Create package dir `src/repodoc/`
- [ ] Add `__init__.py` exposing `__version__ = "0.0.1"`
- [ ] Commit ✔️

### 1.2 Pre-commit Configuration
- [ ] Add `.pre-commit-config.yaml` with:
  - [ ] ruff-format  
  - [ ] black  
  - [ ] ruff-lint  
  - [ ] mypy  
  - [ ] pytest runner  
- [ ] `pre-commit install`
- [ ] Verify `pre-commit run --all-files` passes
- [ ] Commit ✔️

### 1.3 CI Skeleton
- [ ] Create `.github/workflows/ci.yml`
  - [ ] Trigger on `push`, `pull_request` to `main`
  - [ ] Build matrix: py 3.12 & 3.13
  - [ ] Use `actions/setup-python`
  - [ ] Cache `~/.cache/pip`
  - [ ] Steps: install dev deps ➜ lint ➜ type-check ➜ tests ➜ coverage
- [ ] Push & verify CI green
- [ ] Commit ✔️

---

## 2 · CLI Baseline
### 2.1 Typer App Skeleton
- [ ] Create `src/repodoc/cli.py`
  - [ ] `app = typer.Typer(add_completion=False)`
  - [ ] `--version` option
  - [ ] Placeholder `generate` command printing “TODO”
- [ ] Add `entry-points` to `pyproject` (`repodoc = repodoc.cli:app`)
- [ ] Write tests with Typer `CliRunner`
- [ ] Run `pytest -q`
- [ ] Commit ✔️

---

## 3 · Configuration Management
### 3.1 Dataclass & Loader
- [ ] `src/repodoc/config.py`
  - [ ] `@dataclass Config`
  - [ ] `load(cli_args) -> Config` resolution order: file → env → CLI
  - [ ] Validate Ollama URL prefix
- [ ] Add custom `ConfigurationError`
- [ ] Unit-test precedence matrix (16 permutations)
- [ ] Commit ✔️

---

## 4 · Repomix Parsing
### 4.1 Parser MVP
- [ ] Define `Snippet` dataclass (`name`, `language`, `content`)
- [ ] Implement `parse(path: Path) -> list[Snippet]`
- [ ] Create fixtures: valid, missing header, malformed separator
- [ ] Raise `InputFileError` on failure cases
- [ ] Achieve ≥ 95 % branch coverage on parser
- [ ] Commit ✔️

---

## 5 · Error & Exit Codes
- [ ] Create `src/repodoc/errors.py`
  - [ ] Enum `ExitCode` (0–5)
  - [ ] Base `RepodocError(Exception)`
  - [ ] Specific subclasses:
    - [ ] `InputFileError`
    - [ ] `ConfigurationError`
    - [ ] `OllamaConnectionError`
    - [ ] `OutputDirError`
- [ ] Plug initial usage in CLI
- [ ] Commit ✔️

---

## 6 · Ollama Client Stub
### 6.1 Async Wrapper
- [ ] Implement `OllamaClient` (`healthcheck`, `generate`)
- [ ] Use `httpx.AsyncClient`
- [ ] Timeouts: connect=2 s, read=30 s
- [ ] Add global retry strategy (3 attempts, expo backoff)
- [ ] Mock tests with `respx`
- [ ] Commit ✔️

---

## 7 · Documentation Generator Framework
### 7.1 Strategy Registration
- [ ] Create `src/repodoc/generators/base.py`
  - [ ] `DocGenerator` ABC
  - [ ] Registry decorator
- [ ] Implement stubs:
  - [ ] `ApiGenerator`
  - [ ] `ManualGenerator`
  - [ ] `ArchitectureGenerator`
- [ ] Write registry tests
- [ ] Commit ✔️

---

## 8 · Concrete Generators (Prompt-Only Phase)
### 8.1 API Generator
- [ ] Build prompt template focusing on public interfaces
- [ ] Inject `{{snippet_list}}`
- [ ] Return markdown string (no LLM call yet)
- [ ] Snapshot test prompt content
- [ ] Commit ✔️

### 8.2 User Manual Generator
- [ ] Similar steps as API generator
- [ ] Emphasise getting-started examples
- [ ] Commit ✔️

### 8.3 Architecture Generator
- [ ] Prompt emphasising component diagrams (Mermaid placeholders)
- [ ] Commit ✔️

---

## 9 · Writer & Filesystem
- [ ] Implement `writer.write(...)`
- [ ] Map kinds → filenames
- [ ] Ensure atomic write (`path.write_text` to tmp + rename)
- [ ] Tempdir tests for idempotence
- [ ] Commit ✔️

---

## 10 · Progress, Verbose, Logging
- [ ] Create `src/repodoc/logging_utils.py` for Rich handler
- [ ] Add `--verbose / -v` Typer option
- [ ] Use `rich.progress.Progress` for each generation task
- [ ] Unit-test log level switch
- [ ] Commit ✔️

---

## 11 · CLI “Generate” Happy Path
- [ ] Wire together:
  - [ ] Load config  
  - [ ] Health-check Ollama  
  - [ ] Parse repomix  
  - [ ] Instantiate generators per flags  
  - [ ] Call `.generate()` synchronously (mock LLM)  
  - [ ] Write files  
- [ ] Exit `ExitCode.SUCCESS`
- [ ] End-to-end test with CliRunner & tempfs
- [ ] Commit ✔️

---

## 12 · Failure-Path Behaviour
- [ ] Offline Ollama ⇒ exit 4, error logged, continue other docs?
- [ ] Missing input file ⇒ exit 3 immediately
- [ ] Unwritable output dir ⇒ exit 5
- [ ] Mixed-flag generation, one fails ⇒ continue others, summary table
- [ ] Parametrised pytest for each scenario
- [ ] Commit ✔️

---

## 13 · LLM Integration
### 13.1 Generate API Requests
- [ ] Implement chunking logic for large prompts (token limit guard)
- [ ] Send `POST /api/generate` (specify `model`, `prompt`)
- [ ] Stream response, accumulate markdown
- [ ] Unit-test with respx streaming mock
- [ ] Commit ✔️

### 13.2 Integration Smoke Test (Live)
- [ ] Spin Ollama locally (`ollama serve`) — docs team machine
- [ ] Run `repodoc generate` against sample repo
- [ ] Manual QA of generated markdown
- [ ] Adjust prompts if quality low
- [ ] Commit updated prompt templates

---

## 14 · Packaging & Distribution
- [ ] Add `scripts/build.sh` to build sdist + wheel
- [ ] Verify `pip install dist/repodoc-*.whl && repodoc --version`
- [ ] Draft `RELEASE.md` with changelog template
- [ ] Update CI workflow to publish on GitHub release tag
- [ ] Commit ✔️

---

## 15 · Documentation & Examples
- [ ] Create `README.md` with badges, usage, architecture diagram
- [ ] Add `docs/usage_example.gif` screencast
- [ ] Include Mermaid diagrams in Architecture docs
- [ ] Commit ✔️

---

## 16 · Quality Gates
- [ ] Coverage ≥ 90 % (`pytest --cov=repodoc`)
- [ ] Lint errors 0
- [ ] mypy strict passes
- [ ] Dependabot enabled
- [ ] Security scan (Bandit) passes
- [ ] Commit ✔️

---

## 17 · Release v0.1.0
- [ ] Update `__version__` → 0.1.0
- [ ] Tag `git tag -a v0.1.0 -m "Initial release"`
- [ ] Push tags, verify release action uploads artifacts
- [ ] Create GitHub release notes
- [ ] Announce internally

---

## 18 · Post-Release Enhancements (Backlog)
- [ ] Async generation pipeline (concurrent docs)
- [ ] Add `--openapi` flag for OpenAPI-based docs
- [ ] Web UI wrapper (FastAPI + React)
- [ ] Plugin system for custom generators
- [ ] Docker image publish

---

**Tip:** Copy this file as `todo.md` at repo root and tick boxes as you progress.  
Happy shipping 🚀
