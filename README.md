# adf-core-python

## Documentation

[ADF Core Python Documentation](https://adf-python.github.io/adf-core-python/)

## Development Environment

### Prerequisites

- Python (3.13 or higher)
- uv (0.8.2 or higher)

### Installation

```bash
uv sync
```

### Run Agent

```bash
uv run python ./src/adf_core_python/launcher.py

# get help
uv run python ./src/adf_core_python/launcher.py -h
```

### Build

```bash
uv build
```

### Pre Commit

```bash
uv run ruff format .
uv run ruff check .
uv run mypy .
```
