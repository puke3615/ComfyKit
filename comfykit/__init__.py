"""ComfyKit - ComfyUI Python SDK for developers

ComfyKit provides a simple, Pythonic API for executing ComfyUI workflows.

Example:
    >>> from comfykit import ComfyKit
    >>> 
    >>> kit = ComfyKit()
    >>> result = await kit.execute("workflow.json", {"prompt": "a cat"})
    >>> print(result.images)
"""

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Python 3.8-3.10

from pathlib import Path

from comfykit.comfyui.models import ExecuteResult

# Core API exports
from comfykit.executor import ComfyKit


def get_version() -> str:
    """Get the version from multiple sources"""
    # Method 1: Try to get version from installed package metadata (works for uvx/pip)
    try:
        from importlib.metadata import version
        return version("comfykit")
    except Exception:
        pass

    # Method 2: Try to get version from pyproject.toml (works for development)
    try:
        # Find the pyproject.toml file in multiple possible locations
        current_dir = Path(__file__).parent
        possible_paths = [
            # For development environment (project root)
            current_dir.parent / "pyproject.toml",
            # For installed package (included in package)
            current_dir / "pyproject.toml",
            # For uvx/pip installed package (in site-packages)
            current_dir / ".." / "pyproject.toml",
        ]

        pyproject_path = None
        for path in possible_paths:
            if path.exists():
                pyproject_path = path
                break

        if pyproject_path is None:
            return "unknown"

        with open(pyproject_path, "rb") as f:
            pyproject_data = tomllib.load(f)

        return pyproject_data.get("project", {}).get("version", "unknown")
    except Exception:
        return "unknown"

__version__ = get_version()

__all__ = [
    "ComfyKit",
    "ExecuteResult",
    "__version__",
]
