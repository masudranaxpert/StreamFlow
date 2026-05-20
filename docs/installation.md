# Installation

## Requirements

- Python 3.10 or higher
- pip

## Install from GitHub

```bash
pip install git+https://github.com/masudranaxpert/StreamFlow.git
```

## Install from Source

```bash
git clone https://github.com/masudranaxpert/StreamFlow.git
cd StreamFlow
pip install -e .
```

## Development Install

For development with all dev dependencies:

```bash
git clone https://github.com/masudranaxpert/StreamFlow.git
cd StreamFlow
pip install -e ".[dev]"
```

## Dependencies

Core dependencies (installed automatically):
- `httpx>=0.27.0` - HTTP client
- `rich>=15.0.0` - Terminal formatting
- `pycryptodome>=3.20.0` - AES encryption for master link decryption

## Verify Installation

```bash
streamflow help
```

Or in Python:

```python
import streamflow
print(f"StreamFlow version: {streamflow.__version__}")
```