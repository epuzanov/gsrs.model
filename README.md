# gsrs-model

`gsrs-model` provides Pydantic v2 models for GSRS substance records.

## Features

- Installable Python package exposing `gsrs.model`
- Pydantic v2-compatible models generated from the GSRS schema and refined for live GSRS payloads
- `Substance` dispatches automatically to the correct concrete subclass based on `substanceClass`
- Lightweight test suite for imports, serialization, and dispatch behavior

## Installation

```bash
pip install .
```

For local development:

```bash
pip install -e .
```

## Build

Build source and wheel distributions with:

```bash
python -m build
```

If the `build` package is not installed yet:

```bash
pip install build
```

The generated artifacts are written to `dist/`.

## Usage

```python
from gsrs.model import Substance

payload = {
    "substanceClass": "concept",
    "names": [
        {
            "name": "Example Substance",
            "type": "cn",
            "languages": ["en"],
            "nameJurisdiction": [],
            "nameOrgs": [],
            "references": [],
            "access": [],
        }
    ],
    "references": [
        {
            "docType": "SYSTEM",
            "citation": "generated",
            "publicDomain": True,
            "tags": [],
            "access": [],
        }
    ],
    "version": "1",
}

substance = Substance.model_validate(payload)
print(type(substance).__name__)
print(substance.model_dump_json())
```

## Development

Run tests with:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Run a compile check with:

```bash
python -m compileall gsrs
```

## License

MIT. See [LICENSE](LICENSE).
