# ComfyKit

> **ComfyUI - UI + Kit = ComfyKit**
>
> Python SDK for ComfyUI - Support Local or Cloud - Generate images, videos, audio in 3 lines

<div align="center">
  <a href="https://pypi.org/project/comfykit/">
    <img src="https://badge.fury.io/py/comfykit.svg" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/comfykit/">
    <img src="https://img.shields.io/pypi/pyversions/comfykit.svg" alt="Python">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="https://github.com/puke3615/ComfyKit">
    <img src="https://img.shields.io/github/stars/puke3615/ComfyKit?style=social" alt="GitHub stars">
  </a>
  <a href="https://github.com/puke3615/ComfyKit">
    <img src="https://img.shields.io/github/last-commit/puke3615/ComfyKit" alt="GitHub last commit">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/puke3615/ComfyKit/pulls">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
  </a>

  <p>
    <a href="https://puke3615.github.io/ComfyKit/"><strong>📖 Documentation</strong></a> | 
    <a href="#-quick-start"><strong>🚀 Quick Start</strong></a> | 
    <a href="#️-workflow-dsl-quick-reference"><strong>🎯 DSL Reference</strong></a> | 
    <a href="https://github.com/puke3615/ComfyKit/tree/main/examples"><strong>💡 Examples</strong></a> | 
    <a href="https://github.com/puke3615/ComfyKit/issues"><strong>❓ Issues</strong></a>
  </p>
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

## 🔍 ComfyKit vs ComfyUI Native API

| Aspect | ComfyUI Native API | ComfyKit |
|--------|-------------------|----------|
| **Complexity** | Manual WebSocket/HTTP handling | 3 lines of code |
| **Return Value** | Raw JSON, need to parse yourself | Structured `ExecuteResult` object |
| **Media Handling** | Need to construct URLs manually | Automatically generates complete media URLs |
| **Error Handling** | Need to implement yourself | Built-in comprehensive error handling |
| **Best For** | Familiar with ComfyUI internals | Just want quick integration |

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
  <p><strong>If ComfyKit helps you, please give it a ⭐ Star!</strong></p>
  <p>
    <a href="https://github.com/puke3615/ComfyKit">GitHub</a> · 
    <a href="https://pypi.org/project/comfykit/">PyPI</a> · 
    <a href="https://github.com/puke3615/ComfyKit/issues">Issues</a>
  </p>
</div>

