# ComfyKit

> **ComfyUI - UI + Kit = ComfyKit**
>
> 面向开发者的 ComfyUI Python SDK，支持本地或云端，3 行代码生成图像、视频、音频

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
</div>

---

## ✨ ComfyKit 是什么？

**ComfyKit 是一个纯粹的 Python SDK**，提供简洁的 API 来执行 ComfyUI workflows，返回结构化的 Python 对象。

### 3 行代码执行一个 workflow

```python
from comfykit import ComfyKit

kit = ComfyKit()
result = await kit.execute("workflow.json", {"prompt": "a cute cat"})

print(result.images)  # ['http://127.0.0.1:8188/view?filename=cat_001.png']
```

### 获得结构化的返回数据

```python
# ExecuteResult 对象，不是字符串！
result.status          # "completed"
result.images          # 所有生成的图片 URL
result.images_by_var   # 按变量名分组的图片
result.videos          # 视频 URL（如果有）
result.audios          # 音频 URL（如果有）
result.duration        # 执行耗时
```

---

## 🎯 核心特性

- ⚡ **零配置开箱即用**：默认连接本地 ComfyUI (`http://127.0.0.1:8188`)
- ☁️ **云端执行支持**：无缝对接 RunningHub 云平台 - **无需 GPU 或本地 ComfyUI**
- 🎨 **极简 API**：3 行代码执行 workflow，无需理解内部实现
- 📊 **结构化输出**：返回 `ExecuteResult` 对象，而非字符串
- 🔄 **智能识别**：自动识别本地文件、URL 或 RunningHub workflow ID
- 🔌 **轻量级**：核心依赖少于 10 个
- 🎭 **多模态支持**：图像、视频、音频一站式支持

---

## 🔍 ComfyKit vs ComfyUI 原生 API

| 方面 | ComfyUI 原生 API | ComfyKit |
|--------|-------------------|----------|
| **复杂度** | 需要手动处理 WebSocket/HTTP | 3 行代码搞定 |
| **返回值** | 原始 JSON，需要自己解析 | 结构化 `ExecuteResult` 对象 |
| **媒体处理** | 需要手动构造 URL | 自动生成完整的媒体 URL |
| **错误处理** | 需要自己实现 | 内置完善的错误处理 |
| **适合人群** | 熟悉 ComfyUI 内部机制 | 只想快速集成 |

---

## 🙏 致谢

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 强大的 AI 图像生成框架
- [RunningHub](https://www.runninghub.ai) - ComfyUI 云平台

---

## 📞 联系方式

- 作者：Fan Wu
- 邮箱：1129090915@qq.com
- GitHub：[@puke3615](https://github.com/puke3615)

---

<div align="center">
  <p><strong>如果 ComfyKit 对你有帮助，请给个 ⭐ Star！</strong></p>
  <p>
    <a href="https://github.com/puke3615/ComfyKit">GitHub</a> · 
    <a href="https://pypi.org/project/comfykit/">PyPI</a> · 
    <a href="https://github.com/puke3615/ComfyKit/issues">Issues</a>
  </p>
</div>

