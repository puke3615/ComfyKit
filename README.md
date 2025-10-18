# ComfyKit

> **ComfyUI - UI + Kit = ComfyKit**
>
> Python SDK for ComfyUI - Support Local or Cloud - Generate images, videos, audio in 3 lines

<div align="center">

**English** | [中文](README_CN.md)

[![PyPI version](https://badge.fury.io/py/comfykit.svg)](https://pypi.org/project/comfykit/)
[![Python](https://img.shields.io/pypi/pyversions/comfykit.svg)](https://pypi.org/project/comfykit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## ✨ What is ComfyKit?

**ComfyKit is a pure Python SDK** that provides a clean API for executing ComfyUI workflows and returns structured Python objects.

### Execute a workflow in 3 lines of code

```python
from comfykit import ComfyKit

kit = ComfyKit()
result = await kit.execute("workflow.json", {"prompt": "a cute cat"})

print(result.images)  # ['http://127.0.0.1:8188/view?filename=cat_001.png']
```

### Get structured data back

```python
# ExecuteResult object, not strings!
result.status          # "completed"
result.images          # All generated image URLs
result.images_by_var   # Images grouped by variable name
result.videos          # Video URLs (if any)
result.audios          # Audio URLs (if any)
result.duration        # Execution time
```

---

## 🎯 Key Features

- ⚡ **Zero Configuration**: Works out of the box, connects to local ComfyUI by default (`http://127.0.0.1:8188`)
- ☁️ **Cloud Execution**: Seamless RunningHub cloud support - **No GPU or local ComfyUI needed**
- 🎨 **Simple API**: 3 lines of code to execute workflows, no need to understand internals
- 📊 **Structured Output**: Returns `ExecuteResult` objects, not strings
- 🔄 **Smart Detection**: Auto-detects local files, URLs, and RunningHub workflow IDs
- 🔌 **Lightweight**: Less than 10 core dependencies
- 🎭 **Multimodal Support**: Images, videos, audio - all in one place

---

## 📦 Installation

### Using pip

```bash
pip install comfykit
```

### Using uv (recommended)

```bash
uv add comfykit
```

---

## 🚀 Quick Start

### Option 1: RunningHub Cloud (No GPU needed) ⭐

If you don't have a local GPU or ComfyUI environment, use RunningHub cloud:

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # Initialize with RunningHub (only API key needed)
    kit = ComfyKit(
        runninghub_api_key="your-runninghub-key"
    )
    
    # Execute with workflow ID
    result = await kit.execute("12345", {
        "prompt": "a beautiful sunset over the ocean"
    })
    
    print(f"🖼️  Generated images: {result.images}")

asyncio.run(main())
```

> 💡 **Tip**: Get your free API key at [RunningHub](https://www.runninghub.ai)

### Option 2: Local ComfyUI

If you have ComfyUI running locally:

#### 1. Start ComfyUI

```bash
# Start ComfyUI (default port 8188)
python main.py
```

#### 2. Execute workflow

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # Initialize (uses default config)
    kit = ComfyKit()
    
    # Execute workflow
    result = await kit.execute(
        "workflow.json",
        params={"prompt": "a cute cat playing with yarn"}
    )
    
    # Check results
    if result.status == "completed":
        print(f"✅ Success! Duration: {result.duration:.2f}s")
        print(f"🖼️  Images: {result.images}")
    else:
        print(f"❌ Failed: {result.msg}")

asyncio.run(main())
```

---

## 📚 Usage Examples

### Execute local ComfyUI workflow

```python
from comfykit import ComfyKit

# Connect to local ComfyUI (default)
kit = ComfyKit()

# Execute local workflow file
result = await kit.execute("workflow.json", {
    "prompt": "a cat",
    "seed": 42,
    "steps": 20
})
```

### Custom ComfyUI server

```python
# Connect to remote ComfyUI server
kit = ComfyKit(
    comfyui_url="http://my-server:8188",
    api_key="your-api-key"  # If authentication is required
)
```

### RunningHub cloud execution

```python
# Use RunningHub cloud (no local ComfyUI needed)
kit = ComfyKit(
    runninghub_api_key="your-runninghub-key"
)

# Execute with workflow ID
result = await kit.execute("12345", {
    "prompt": "a beautiful landscape"
})
```

### Execute remote workflow URL

```python
# Automatically download and execute
result = await kit.execute(
    "https://example.com/workflow.json",
    {"prompt": "a cat"}
)
```

### Execute workflow from dict

```python
workflow_dict = {
    "nodes": [...],
    "edges": [...]
}

result = await kit.execute_json(workflow_dict, {
    "prompt": "a cat"
})
```

### Process results

```python
result = await kit.execute("workflow.json", {"prompt": "a cat"})

# Basic info
print(f"Status: {result.status}")           # completed / failed
print(f"Duration: {result.duration}s")      # 3.45
print(f"Prompt ID: {result.prompt_id}")     # uuid

# Generated media files
print(f"Images: {result.images}")           # ['http://...']
print(f"Videos: {result.videos}")           # ['http://...']
print(f"Audios: {result.audios}")           # ['http://...']

# Grouped by variable name (if workflow defines output variables)
print(f"Cover: {result.images_by_var['cover']}")
print(f"Thumbnail: {result.images_by_var['thumbnail']}")
```

---

## ⚙️ Configuration

### Configuration Priority

ComfyKit uses the following priority for configuration:

1. **Constructor parameters** (highest priority)
2. **Environment variables**
3. **Default values**

### Local ComfyUI configuration

```python
kit = ComfyKit(
    # ComfyUI server URL
    comfyui_url="http://127.0.0.1:8188",  # Default
    
    # Execution mode: http (recommended) or websocket
    executor_type="http",  # Default
    
    # API Key (if ComfyUI requires authentication)
    api_key="your-api-key",
    
    # Cookies (if needed)
    cookies="session=abc123"
)
```

### RunningHub cloud configuration

```python
kit = ComfyKit(
    # RunningHub API URL
    runninghub_url="https://www.runninghub.ai",  # Default
    
    # RunningHub API Key (required)
    runninghub_api_key="rh-key-xxx",
    
    # Timeout (seconds)
    runninghub_timeout=300,  # Default: 5 minutes
    
    # Retry count
    runninghub_retry_count=3  # Default: 3 retries
)
```

### Environment variables

```bash
# ComfyUI configuration
export COMFYUI_BASE_URL="http://127.0.0.1:8188"
export COMFYUI_EXECUTOR_TYPE="http"
export COMFYUI_API_KEY="your-api-key"
export COMFYUI_COOKIES="session=abc123"

# RunningHub configuration
export RUNNINGHUB_BASE_URL="https://www.runninghub.ai"
export RUNNINGHUB_API_KEY="rh-key-xxx"
export RUNNINGHUB_TIMEOUT="300"
export RUNNINGHUB_RETRY_COUNT="3"
```

---

## 🔍 ComfyKit vs ComfyUI Native API

| Aspect | ComfyUI Native API | ComfyKit |
|--------|-------------------|----------|
| **Complexity** | Manual WebSocket/HTTP handling | 3 lines of code |
| **Return Value** | Raw JSON, need to parse yourself | Structured `ExecuteResult` object |
| **Media Handling** | Need to construct URLs manually | Automatically generates complete media URLs |
| **Error Handling** | Need to implement yourself | Built-in comprehensive error handling |
| **Best For** | Familiar with ComfyUI internals | Just want quick integration |

---

## 📖 API Reference

### ComfyKit Class

```python
class ComfyKit:
    def __init__(
        self,
        # Local ComfyUI configuration
        comfyui_url: Optional[str] = None,
        executor_type: Literal["http", "websocket"] = "http",
        api_key: Optional[str] = None,
        cookies: Optional[str] = None,
        
        # RunningHub cloud configuration
        runninghub_url: Optional[str] = None,
        runninghub_api_key: Optional[str] = None,
        runninghub_timeout: int = 300,
        runninghub_retry_count: int = 3,
    ):
        """Initialize ComfyKit
        
        All parameters are optional and can be configured via environment variables
        """
        
    async def execute(
        self,
        workflow: Union[str, Path],
        params: Optional[Dict[str, Any]] = None,
    ) -> ExecuteResult:
        """Execute workflow
        
        Args:
            workflow: Workflow source, can be:
                     - Local file path: "workflow.json"
                     - RunningHub ID: "12345" (numeric)
                     - Remote URL: "https://example.com/workflow.json"
            params: Workflow parameters, e.g. {"prompt": "a cat", "seed": 42}
        
        Returns:
            ExecuteResult: Structured execution result
        """
        
    async def execute_json(
        self,
        workflow_json: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> ExecuteResult:
        """Execute workflow from JSON dict
        
        Args:
            workflow_json: Workflow JSON dict
            params: Workflow parameters
        
        Returns:
            ExecuteResult: Structured execution result
        """
```

### ExecuteResult Class

```python
class ExecuteResult:
    """Workflow execution result"""
    
    status: str                           # Execution status: "completed" / "failed"
    prompt_id: Optional[str]              # Prompt ID
    duration: Optional[float]             # Execution duration (seconds)
    
    # Media outputs
    images: List[str]                     # All image URLs
    videos: List[str]                     # All video URLs
    audios: List[str]                     # All audio URLs
    texts: List[str]                      # All text outputs
    
    # Grouped by variable name
    images_by_var: Dict[str, List[str]]   # Images grouped by variable name
    videos_by_var: Dict[str, List[str]]   # Videos grouped by variable name
    audios_by_var: Dict[str, List[str]]   # Audios grouped by variable name
    texts_by_var: Dict[str, List[str]]    # Texts grouped by variable name
    
    # Raw outputs
    outputs: Optional[Dict[str, Any]]     # Raw output data
    msg: Optional[str]                    # Error message (if failed)
```

---

## 📂 More Examples

The project includes complete example code in the `examples/` directory:

- [`01_quick_start.py`](examples/01_quick_start.py) - Quick start guide
- [`02_configuration.py`](examples/02_configuration.py) - Configuration options
- [`03_local_workflows.py`](examples/03_local_workflows.py) - Local workflow execution
- [`04_runninghub_cloud.py`](examples/04_runninghub_cloud.py) - RunningHub cloud execution
- [`05_advanced_features.py`](examples/05_advanced_features.py) - Advanced features

Run all examples:

```bash
cd examples
python run_all.py
```

---

## 🛠️ Development

### Install development dependencies

```bash
uv sync --extra dev
```

### Run tests

```bash
pytest
```

### Code formatting

```bash
ruff check --fix
ruff format
```

---

## 🤝 Contributing

Contributions are welcome! Please check [Issues](https://github.com/puke3615/ComfyKit/issues) for areas that need help.

### Contribution Process

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - Powerful AI image generation framework
- [RunningHub](https://www.runninghub.ai) - ComfyUI cloud platform

---

## 📞 Contact

- Author: Fan Wu
- Email: 1129090915@qq.com
- GitHub: [@puke3615](https://github.com/puke3615)

---

<div align="center">

**If ComfyKit helps you, please give it a ⭐ Star!**

[GitHub](https://github.com/puke3615/ComfyKit) · [PyPI](https://pypi.org/project/comfykit/) · [Issues](https://github.com/puke3615/ComfyKit/issues)

</div>
