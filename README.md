# ComfyKit

> **ComfyUI - UI + Kit = ComfyKit**
>
> Python SDK for ComfyUI - Support Local or Cloud - Generate images, videos, audio in 3 lines

<div align="center">

**English** | [中文](README_CN.md)

[![PyPI version](https://badge.fury.io/py/comfykit.svg)](https://pypi.org/project/comfykit/)
[![Python](https://img.shields.io/pypi/pyversions/comfykit.svg)](https://pypi.org/project/comfykit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/puke3615/ComfyKit?style=social)](https://github.com/puke3615/ComfyKit)
[![GitHub last commit](https://img.shields.io/github/last-commit/puke3615/ComfyKit)](https://github.com/puke3615/ComfyKit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/puke3615/ComfyKit/pulls)

[**📖 Documentation**](https://puke3615.github.io/ComfyKit/) | 
[**🚀 Quick Start**](#-quick-start) | 
[**🎯 DSL Reference**](#️-workflow-dsl-quick-reference) | 
[**💡 Examples**](examples/) | 
[**❓ Issues**](https://github.com/puke3615/ComfyKit/issues)

</div>

---

## ✨ What is ComfyKit?

**ComfyKit is a pure Python SDK** that provides a clean API for executing ComfyUI workflows and returns structured Python objects.

### Execute a workflow in 3 lines of code

```python
from comfykit import ComfyKit

# Connect to local ComfyUI server
kit = ComfyKit(comfyui_url="http://127.0.0.1:8188")
result = await kit.execute("workflow.json", {"prompt": "a cute cat"})

print(result.images)  # ['http://127.0.0.1:8188/view?filename=cat_001.png']

# 🌐 Or use RunningHub cloud (no local GPU needed)
# kit = ComfyKit(runninghub_api_key="rh-xxx")
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
    # Connect to local ComfyUI (default: http://127.0.0.1:8188)
    kit = ComfyKit(comfyui_url="http://127.0.0.1:8188")
    
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

> 💡 **Tip**: `comfyui_url` defaults to `http://127.0.0.1:8188` and can be omitted

---

## 📚 Usage Examples

### Execute local ComfyUI workflow

```python
from comfykit import ComfyKit

# Connect to local ComfyUI
kit = ComfyKit(comfyui_url="http://127.0.0.1:8188")  # Default, can be omitted

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

## 🏷️ Workflow DSL Quick Reference

ComfyKit provides a concise DSL (Domain Specific Language) for marking workflow nodes, allowing you to:
- Define dynamic parameters
- Mark output variables
- Specify required/optional parameters
- Automatically handle media file uploads

### DSL Syntax Quick Reference

These DSL markers are written in the **title field of ComfyUI workflow nodes** to convert fixed workflows into parameterizable templates.

**Usage Steps**:
1. In ComfyUI editor, double-click a node and modify its title to add DSL markers (e.g., `$prompt.text!`)
2. Save as **API format JSON** (select "Save (API Format)" from menu, not regular "Save")
3. Execute with parameters via `kit.execute("workflow.json", {"prompt": "value"})`

> ⚠️ **Important**: ComfyKit requires API format workflow JSON, not UI format.

| Syntax | Description | Example | Effect |
|--------|-------------|---------|--------|
| `$param` | Basic parameter (shorthand) | `$prompt` | Parameter `prompt`, maps to field `prompt` |
| `$param.field` | Specify field mapping | `$prompt.text` | Parameter `prompt`, maps to field `text` |
| `$param!` | Required parameter | `$prompt!` | Parameter `prompt` is required, no default |
| `$~param` | Media parameter (upload) | `$~image` | Parameter `image` requires file upload |
| `$~param!` | Required media parameter | `$~image!` | Parameter `image` is required and needs upload |
| `$param.~field!` | Combined markers | `$img.~image!` | Parameter `img` maps to `image`, required and upload |
| `$output.name` | Output variable marker | `$output.cover` | Mark output variable name as `cover` |
| `Text, $p1, $p2` | Multiple parameters | `Size, $width!, $height!` | Define multiple parameters in one node |

### Parameter Marking Examples

#### 1. Text Prompt Parameter

In a ComfyUI workflow CLIPTextEncode node:

```json
{
  "6": {
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "$prompt.text!"
    },
    "inputs": {
      "text": "a beautiful landscape",
      "clip": ["4", 1]
    }
  }
}
```

**Marker explanation**:
- `$prompt` - Parameter name is `prompt`
- `.text` - Maps to node's `text` field
- `!` - Required parameter, must be provided

**Usage**:
```python
result = await kit.execute("workflow.json", {
    "prompt": "a cute cat"  # Replaces inputs.text value
})
```

#### 2. Image Upload Parameter

In a LoadImage node:

```json
{
  "10": {
    "class_type": "LoadImage",
    "_meta": {
      "title": "$~input_image!"
    },
    "inputs": {
      "image": "default.png"
    }
  }
}
```

**Marker explanation**:
- `$~input_image!` - Parameter `input_image`, needs upload (`~`), required (`!`)
- ComfyKit handles file upload automatically

**Usage**:
```python
result = await kit.execute("workflow.json", {
    "input_image": "/path/to/cat.jpg"  # Automatically uploads to ComfyUI
})
```

#### 3. Multiple Parameters in One Node

```json
{
  "5": {
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Size, $width!, $height!"
    },
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    }
  }
}
```

**Marker explanation**:
- `Size` - Display text, not a parameter
- `$width!` - Required parameter `width` (shorthand, maps to same field)
- `$height!` - Required parameter `height`

**Usage**:
```python
result = await kit.execute("workflow.json", {
    "width": 1024,
    "height": 768
})
```

#### 4. Optional Parameters (with defaults)

```json
{
  "3": {
    "class_type": "KSampler",
    "_meta": {
      "title": "Sampler, $seed, $steps"
    },
    "inputs": {
      "seed": 0,          # Default value 0
      "steps": 20,        # Default value 20
      "cfg": 8.0,
      "model": ["4", 0]
    }
  }
}
```

**Marker explanation**:
- `$seed` and `$steps` have no `!`, they are optional
- If not provided, uses default values from workflow

**Usage**:
```python
# Use defaults
result = await kit.execute("workflow.json", {})

# Override some parameters
result = await kit.execute("workflow.json", {
    "seed": 42  # Only override seed, steps uses default 20
})
```

### Output Marking Examples

#### 1. Using Output Variable Marker

```json
{
  "9": {
    "class_type": "SaveImage",
    "_meta": {
      "title": "$output.cover"
    },
    "inputs": {
      "filename_prefix": "book_cover",
      "images": ["8", 0]
    }
  }
}
```

**Marker explanation**:
- `$output.cover` - Mark this node's output as `cover` variable

**Usage**:
```python
result = await kit.execute("workflow.json", params)

# Access output by variable name
cover_images = result.images_by_var["cover"]
print(f"Cover image: {cover_images[0]}")
```

#### 2. Multiple Output Variables

```json
{
  "9": {
    "class_type": "SaveImage",
    "_meta": {
      "title": "$output.cover"
    }
  },
  "15": {
    "class_type": "SaveImage",
    "_meta": {
      "title": "$output.thumbnail"
    }
  }
}
```

**Usage**:
```python
result = await kit.execute("workflow.json", params)

# Get different outputs separately
cover = result.images_by_var["cover"][0]
thumbnail = result.images_by_var["thumbnail"][0]
```

#### 3. Automatic Output Recognition (no marker needed)

If you don't use `$output.xxx` markers, ComfyKit auto-detects output nodes:

```json
{
  "9": {
    "class_type": "SaveImage",
    "_meta": {
      "title": "Final Output"
    }
  }
}
```

**Usage**:
```python
result = await kit.execute("workflow.json", params)

# All images are in the images list
all_images = result.images

# Access by node ID
images_from_node_9 = result.images_by_var["9"]
```

### DSL Best Practices

1. **Parameter Naming**: Use descriptive names like `$positive_prompt` instead of `$p`
2. **Required Markers**: Use `!` for parameters with no reasonable default
3. **Upload Markers**: Use `~` for image, video, audio parameters
4. **Output Variables**: Use `$output.xxx` for important outputs to make them easy to reference
5. **Display Text**: Add descriptive text in multi-param markers, e.g. `"Size, $width!, $height!"`

### Complete Example

A complete Text-to-Image workflow with DSL markers:

```json
{
  "4": {
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "$model.ckpt_name"
    },
    "inputs": {
      "ckpt_name": "sd_xl_base_1.0.safetensors"
    }
  },
  "5": {
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Canvas, $width!, $height!"
    },
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    }
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "$prompt.text!"
    },
    "inputs": {
      "text": "a beautiful landscape",
      "clip": ["4", 1]
    }
  },
  "9": {
    "class_type": "SaveImage",
    "_meta": {
      "title": "$output.result"
    },
    "inputs": {
      "filename_prefix": "output",
      "images": ["8", 0]
    }
  }
}
```

**Execution**:
```python
result = await kit.execute("t2i_workflow.json", {
    "prompt": "a cute cat playing with yarn",
    "width": 1024,
    "height": 768,
    "model": "dreamshaper_8.safetensors"  # Optional, has default
})

# Get result
output_image = result.images_by_var["result"][0]
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
