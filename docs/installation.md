# Installation

## Requirements

- Python 3.10 or higher
- pip (or poetry, pdm, etc.)

## Install from PyPI

```bash
pip install streamflow
```

## Install from Source

```bash
git clone https://github.com/username/streamflow
cd streamflow
pip install -e .
```

## Development Install

For development with all dev dependencies:

```bash
git clone https://github.com/username/streamflow
cd streamflow
pip install -e ".[dev]"
```

## Dependencies

Core dependencies (installed automatically):
- `httpcloak>=1.6.6` - HTTP client
- `rich>=15.0.0` - Terminal formatting
- `pycryptodome>=3.20.0` - AES encryption for master link decryption

## Verify Installation

```python
import streamflow
from streamflow.platforms.streamembed import get_master_link

# Quick test
result = get_master_link("test")
print(f"StreamFlow installed: {result}")
```