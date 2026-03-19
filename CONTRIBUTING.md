# Contributing

## Setup

```bash
pip install -e .
```

## Checks

```bash
python -m unittest discover -s tests -p "test_*.py"
python -m compileall gsrs
```

## Guidelines

- Keep generated model style consistent across files.
- Prefer schema-backed typing changes over ad hoc exceptions.
- Add or update tests when changing package exports or validation behavior.
- Avoid committing local environment or build artifacts.
