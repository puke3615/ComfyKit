# Development

Guide for ComfyKit development.

## Install Development Dependencies

```bash
uv sync --extra dev
```

## Run Tests

```bash
pytest
```

## Code Formatting

```bash
ruff check --fix
ruff format
```

## Project Structure

```
ComfyKit/
├── comfykit/           # Main package
│   ├── comfyui/        # ComfyUI integration
│   └── utils/          # Utilities
├── examples/           # Example scripts
├── workflows/          # Example workflows
└── tests/              # Test suite
```

## Next Steps

- Check [Contributing](contributing.md) guide
- Read [API Reference](api-reference.md)

