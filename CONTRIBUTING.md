# Contributing to AudioDatasetAudit

Thank you for your interest in contributing.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Run tests

```bash
pytest
```

## Lint

```bash
ruff check .
```

## What to contribute

Helpful contribution areas include:
- new audit checks
- test cases for edge conditions
- documentation improvements
- report formatting improvements
- public dataset examples

## Contribution style

Please prefer small, focused pull requests with tests and clear descriptions.
