# Installation

## Requirements

- Python 3.10 or higher
- pip or uv package manager

## Install via pip

```bash
pip install comfykit
```

## Install via uv (recommended)

```bash
uv add comfykit
```

## Verify Installation

```python
from comfykit import ComfyKit

print("ComfyKit installed successfully!")
```

## Optional Dependencies

### Development Dependencies

If you want to contribute to ComfyKit, install development dependencies:

```bash
pip install comfykit[dev]
```

Or with uv:

```bash
uv sync --extra dev
```

This includes:
- pytest - Testing framework
- pytest-asyncio - Async test support
- black - Code formatter
- ruff - Linter

## Next Steps

After installation, check out the [Quick Start](quick-start.md) guide to begin using ComfyKit.

