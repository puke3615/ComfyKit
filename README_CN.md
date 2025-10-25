# ComfyKit

> **ComfyUI - UI + Kit = ComfyKit**
>
> 面向开发者的 ComfyUI Python SDK，支持本地或云端，3 行代码生成图像、视频、音频

<div align="center">

[English](README.md) | **中文**

[![PyPI version](https://badge.fury.io/py/comfykit.svg)](https://pypi.org/project/comfykit/)
[![Python](https://img.shields.io/pypi/pyversions/comfykit.svg)](https://pypi.org/project/comfykit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/puke3615/ComfyKit?style=social)](https://github.com/puke3615/ComfyKit)
[![GitHub last commit](https://img.shields.io/github/last-commit/puke3615/ComfyKit)](https://github.com/puke3615/ComfyKit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/puke3615/ComfyKit/pulls)

[**📖 在线文档**](https://puke3615.github.io/ComfyKit/) | 
[**🚀 快速开始**](#-快速开始) | 
[**🎯 DSL 标记**](#️-workflow-dsl-标记速查表) | 
[**💡 示例代码**](examples/) | 
[**❓ 问题反馈**](https://github.com/puke3615/ComfyKit/issues)

</div>


---

## ✨ ComfyKit 是什么？

**ComfyKit 是一个纯粹的 Python SDK**，提供简洁的 API 来执行 ComfyUI workflows，返回结构化的 Python 对象。

### 3 行代码执行一个 workflow

```python
from comfykit import ComfyKit

# Connect to local ComfyUI server
kit = ComfyKit(comfyui_url="http://127.0.0.1:8188")
result = await kit.execute("workflow.json", {"prompt": "a cute cat"})

print(result.images)  # ['http://127.0.0.1:8188/view?filename=cat_001.png']

# 🌐 Or use RunningHub cloud (no local GPU needed)
# kit = ComfyKit(runninghub_api_key="rh-xxx")
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

- ⚡ **开箱即用**：零配置，默认连接本地 ComfyUI（`http://127.0.0.1:8188`）
- ☁️ **云端执行**：无缝支持 RunningHub 云平台，**无需本地 GPU 和 ComfyUI 环境**
- 🎨 **简洁 API**：3 行代码执行 workflow，无需了解底层细节
- 📊 **结构化返回**：返回 `ExecuteResult` 对象，不是字符串
- 🔄 **智能识别**：自动识别本地文件、URL、RunningHub workflow ID
- 🔌 **最小依赖**：核心依赖少于 10 个，轻量级
- 🎭 **多模态支持**：图片、视频、音频一站式处理

---

## 📦 安装

### 使用 pip

```bash
pip install comfykit
```

### 使用 uv（推荐）

```bash
uv add comfykit
```

---

## 🚀 快速开始

ComfyKit 支持两种执行方式：**本地 ComfyUI** 和 **RunningHub 云端**。

### 方式 1：本地 ComfyUI（需要本地环境）

#### 1. 启动 ComfyUI

```bash
# 启动 ComfyUI（默认端口 8188）
python main.py
```

#### 2. 准备一个 workflow 文件

```json
{
  "3": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 0,
      "steps": 20,
      "cfg": 8.0,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1.0,
      "model": ["4", 0],
      "positive": ["6", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    }
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "a beautiful landscape",
      "clip": ["4", 1]
    }
  }
  // ... more nodes
}
```

#### 3. 执行 workflow

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # Connect to local ComfyUI (default: http://127.0.0.1:8188)
    kit = ComfyKit(comfyui_url="http://127.0.0.1:8188")
    
    # 执行 workflow
    result = await kit.execute(
        "workflow.json",
        params={"prompt": "a cute cat playing with yarn"}
    )
    
    # 查看结果
    if result.status == "completed":
        print(f"✅ 生成成功！耗时 {result.duration:.2f}s")
        print(f"🖼️  生成的图片：{result.images}")
    else:
        print(f"❌ 生成失败：{result.msg}")

asyncio.run(main())
```

> 💡 **提示**：`comfyui_url` 默认为 `http://127.0.0.1:8188`，可省略此参数

### 方式 2：RunningHub 云端（无需本地环境）⭐

如果你没有本地 GPU 或 ComfyUI 环境，可以使用 RunningHub 云平台：

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # 初始化云端执行（只需 API Key）
    kit = ComfyKit(
        runninghub_api_key="your-runninghub-key"
    )
    
    # 使用 RunningHub workflow ID 执行
    result = await kit.execute("12345", {
        "prompt": "a beautiful landscape"
    })
    
    print(f"🖼️  生成的图片：{result.images}")

asyncio.run(main())
```

> 💡 **提示**：访问 [RunningHub](https://www.runninghub.ai) 获取免费 API Key

---

## 📚 使用示例

### 本地 ComfyUI 执行

```python
from comfykit import ComfyKit

# Connect to local ComfyUI
kit = ComfyKit(comfyui_url="http://127.0.0.1:8188")  # Default, can be omitted

# 执行本地 workflow 文件
result = await kit.execute("workflow.json", {
    "prompt": "a cat",
    "seed": 42,
    "steps": 20
})
```

### 自定义 ComfyUI 地址

```python
# 连接到远程 ComfyUI 服务器
kit = ComfyKit(
    comfyui_url="http://my-server:8188",
    api_key="your-api-key"  # 如果需要认证
)
```

### RunningHub 云端执行

```python
# 使用 RunningHub 云平台（无需本地 ComfyUI）
kit = ComfyKit(
    runninghub_api_key="your-runninghub-key"
)

# 使用 workflow ID 执行
result = await kit.execute("12345", {
    "prompt": "a beautiful landscape"
})
```

### 执行远程 workflow URL

```python
# 自动下载并执行
result = await kit.execute(
    "https://example.com/workflow.json",
    {"prompt": "a cat"}
)
```

### 执行 workflow JSON 字典

```python
workflow_dict = {
    "nodes": [...],
    "edges": [...]
}

result = await kit.execute_json(workflow_dict, {
    "prompt": "a cat"
})
```

### 处理返回结果

```python
result = await kit.execute("workflow.json", {"prompt": "a cat"})

# 基本信息
print(f"状态: {result.status}")           # completed / failed
print(f"耗时: {result.duration}秒")       # 3.45
print(f"Prompt ID: {result.prompt_id}")   # uuid

# 生成的媒体文件
print(f"图片: {result.images}")           # ['http://...']
print(f"视频: {result.videos}")           # ['http://...']
print(f"音频: {result.audios}")           # ['http://...']

# 按变量名分组（如果 workflow 定义了输出变量）
print(f"封面图: {result.images_by_var['cover']}")
print(f"缩略图: {result.images_by_var['thumbnail']}")
```

---

## 🏷️ Workflow DSL 标记速查表

ComfyKit 提供了一套简洁的 DSL（领域特定语言）来标记 workflow 节点，让你能够：
- 定义可传参的动态参数
- 标记输出变量
- 指定必填/可选参数
- 自动处理媒体文件上传

### DSL 语法速查表

这些 DSL 标记写在 **ComfyUI workflow 节点的 title 字段**中，用于将固定的 workflow 转换为可参数化的模板。

**使用步骤**：
1. 在 ComfyUI 编辑器中双击节点，修改 title 添加 DSL 标记（如 `$prompt.text!`）
2. 保存为 **API 格式 JSON**（菜单选择 "Save (API Format)"，不是普通 "Save"）
3. 通过 `kit.execute("workflow.json", {"prompt": "value"})` 传参执行

> ⚠️ **注意**：必须使用 API 格式的 workflow JSON，不是 UI 格式。

| 标记语法 | 说明 | 示例 | 效果 |
|---------|------|------|------|
| `$param` | 基本参数（shorthand） | `$prompt` | 参数名 `prompt`，映射到同名字段 `prompt` |
| `$param.field` | 指定字段映射 | `$prompt.text` | 参数名 `prompt`，映射到字段 `text` |
| `$param!` | 必填参数 | `$prompt!` | 参数 `prompt` 必填，无默认值 |
| `$~param` | 需要上传的媒体参数 | `$~image` | 参数 `image` 需要文件上传 |
| `$~param!` | 必填的媒体参数 | `$~image!` | 参数 `image` 必填且需要上传 |
| `$param.~field!` | 组合标记 | `$img.~image!` | 参数 `img` 映射到 `image` 字段，必填且需上传 |
| `$output.name` | 输出变量标记 | `$output.cover` | 标记输出变量名为 `cover` |
| `Text, $p1, $p2` | 多参数标记 | `Size, $width!, $height!` | 一个节点定义多个参数 |

### 参数标记示例

#### 1. 文本提示词参数

在 ComfyUI workflow 的 CLIPTextEncode 节点中：

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

**标记说明**：
- `$prompt` - 参数名为 `prompt`
- `.text` - 映射到节点的 `text` 字段
- `!` - 必填参数，执行时必须提供

**使用**：
```python
result = await kit.execute("workflow.json", {
    "prompt": "a cute cat"  # 会替换 inputs.text 的值
})
```

#### 2. 图像上传参数

在 LoadImage 节点中：

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

**标记说明**：
- `$~input_image!` - 参数名 `input_image`，需要上传（`~`），必填（`!`）
- ComfyKit 会自动处理文件上传

**使用**：
```python
result = await kit.execute("workflow.json", {
    "input_image": "/path/to/cat.jpg"  # 自动上传到 ComfyUI
})
```

#### 3. 多个参数在一个节点

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

**标记说明**：
- `Size` - 显示文本，不是参数
- `$width!` - 必填参数 `width`（shorthand，映射到同名字段）
- `$height!` - 必填参数 `height`

**使用**：
```python
result = await kit.execute("workflow.json", {
    "width": 1024,
    "height": 768
})
```

#### 4. 可选参数（带默认值）

```json
{
  "3": {
    "class_type": "KSampler",
    "_meta": {
      "title": "Sampler, $seed, $steps"
    },
    "inputs": {
      "seed": 0,          # 默认值 0
      "steps": 20,        # 默认值 20
      "cfg": 8.0,
      "model": ["4", 0]
    }
  }
}
```

**标记说明**：
- `$seed` 和 `$steps` 没有 `!`，是可选参数
- 如果不传参数，使用 workflow 中的默认值

**使用**：
```python
# 使用默认值
result = await kit.execute("workflow.json", {})

# 覆盖部分参数
result = await kit.execute("workflow.json", {
    "seed": 42  # 只覆盖 seed，steps 用默认值 20
})
```

### 输出标记示例

#### 1. 使用输出变量标记

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

**标记说明**：
- `$output.cover` - 标记这个节点的输出为 `cover` 变量

**使用**：
```python
result = await kit.execute("workflow.json", params)

# 通过变量名访问输出
cover_images = result.images_by_var["cover"]
print(f"封面图片: {cover_images[0]}")
```

#### 2. 多个输出变量

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

**使用**：
```python
result = await kit.execute("workflow.json", params)

# 分别获取不同的输出
cover = result.images_by_var["cover"][0]
thumbnail = result.images_by_var["thumbnail"][0]
```

#### 3. 自动输出识别（无需标记）

如果没有使用 `$output.xxx` 标记，ComfyKit 会自动识别输出节点：

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

**使用**：
```python
result = await kit.execute("workflow.json", params)

# 所有图片都在 images 列表中
all_images = result.images

# 按节点 ID 访问
images_from_node_9 = result.images_by_var["9"]
```

### DSL 最佳实践

1. **参数命名**：使用描述性的参数名，如 `$positive_prompt` 而不是 `$p`
2. **必填标记**：对于无合理默认值的参数使用 `!` 标记
3. **上传标记**：对图片、视频、音频等媒体参数使用 `~` 标记
4. **输出变量**：为重要输出使用 `$output.xxx` 命名，便于程序引用
5. **显示文本**：在多参数标记中添加描述文本，如 `"Size, $width!, $height!"`

### 完整示例

一个完整的 Text-to-Image workflow DSL 标记示例：

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

**执行**：
```python
result = await kit.execute("t2i_workflow.json", {
    "prompt": "a cute cat playing with yarn",
    "width": 1024,
    "height": 768,
    "model": "dreamshaper_8.safetensors"  # 可选，有默认值
})

# 获取结果
output_image = result.images_by_var["result"][0]
```

---

## ⚙️ 配置说明

### 配置优先级

ComfyKit 使用以下优先级读取配置：

1. **代码传参**（最高优先级）
2. **环境变量**
3. **默认值**

### ComfyUI 本地执行配置

```python
kit = ComfyKit(
    # ComfyUI 服务器地址
    comfyui_url="http://127.0.0.1:8188",  # 默认值
    
    # 执行模式：http（推荐）或 websocket
    executor_type="http",  # 默认值
    
    # API Key（如果 ComfyUI 开启了认证）
    api_key="your-api-key",
    
    # Cookies（如果需要）
    cookies="session=abc123"
)
```

### RunningHub 云端执行配置

```python
kit = ComfyKit(
    # RunningHub API 地址
    runninghub_url="https://www.runninghub.ai",  # 默认值
    
    # RunningHub API Key（必需）
    runninghub_api_key="rh-key-xxx",
    
    # 超时时间（秒）
    runninghub_timeout=300,  # 默认 5 分钟
    
    # 重试次数
    runninghub_retry_count=3  # 默认 3 次
)
```

### 环境变量配置

```bash
# ComfyUI 配置
export COMFYUI_BASE_URL="http://127.0.0.1:8188"
export COMFYUI_EXECUTOR_TYPE="http"
export COMFYUI_API_KEY="your-api-key"
export COMFYUI_COOKIES="session=abc123"

# RunningHub 配置
export RUNNINGHUB_BASE_URL="https://www.runninghub.ai"
export RUNNINGHUB_API_KEY="rh-key-xxx"
export RUNNINGHUB_TIMEOUT="300"
export RUNNINGHUB_RETRY_COUNT="3"
```

---

## 🔍 ComfyKit vs ComfyUI 原生 API

| 维度 | ComfyUI 原生 API | ComfyKit |
|------|------------------|----------|
| **复杂度** | 需要手动处理 WebSocket/HTTP | 3 行代码执行 |
| **返回值** | 原始 JSON，需要自己解析 | 结构化 `ExecuteResult` 对象 |
| **媒体处理** | 需要手动拼接 URL | 自动生成完整的媒体 URL |
| **云端支持** | 不支持 | 内置 RunningHub 云端执行 |
| **错误处理** | 需要自己实现 | 内置完善的错误处理 |
| **适合人群** | 熟悉 ComfyUI 内部机制 | 只想快速集成 |

---

## 📖 API 参考

### ComfyKit 类

```python
class ComfyKit:
    def __init__(
        self,
        # ComfyUI 本地执行配置
        comfyui_url: Optional[str] = None,
        executor_type: Literal["http", "websocket"] = "http",
        api_key: Optional[str] = None,
        cookies: Optional[str] = None,
        
        # RunningHub 云端执行配置
        runninghub_url: Optional[str] = None,
        runninghub_api_key: Optional[str] = None,
        runninghub_timeout: int = 300,
        runninghub_retry_count: int = 3,
    ):
        """初始化 ComfyKit
        
        所有参数都是可选的，可以通过环境变量配置
        """
        
    async def execute(
        self,
        workflow: Union[str, Path],
        params: Optional[Dict[str, Any]] = None,
    ) -> ExecuteResult:
        """执行 workflow
        
        Args:
            workflow: workflow 来源，可以是：
                     - 本地文件路径: "workflow.json"
                     - RunningHub ID: "12345"（纯数字）
                     - 远程 URL: "https://example.com/workflow.json"
            params: workflow 参数，例如 {"prompt": "a cat", "seed": 42}
        
        Returns:
            ExecuteResult: 结构化的执行结果
        """
        
    async def execute_json(
        self,
        workflow_json: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> ExecuteResult:
        """从 JSON 字典执行 workflow
        
        Args:
            workflow_json: workflow JSON 字典
            params: workflow 参数
        
        Returns:
            ExecuteResult: 结构化的执行结果
        """
```

### ExecuteResult 类

```python
class ExecuteResult:
    """Workflow 执行结果"""
    
    status: str                           # 执行状态: "completed" / "failed"
    prompt_id: Optional[str]              # Prompt ID
    duration: Optional[float]             # 执行耗时（秒）
    
    # 媒体输出
    images: List[str]                     # 所有图片 URL
    videos: List[str]                     # 所有视频 URL
    audios: List[str]                     # 所有音频 URL
    texts: List[str]                      # 所有文本输出
    
    # 按变量名分组的输出
    images_by_var: Dict[str, List[str]]   # 图片按变量名分组
    videos_by_var: Dict[str, List[str]]   # 视频按变量名分组
    audios_by_var: Dict[str, List[str]]   # 音频按变量名分组
    texts_by_var: Dict[str, List[str]]    # 文本按变量名分组
    
    # 原始输出
    outputs: Optional[Dict[str, Any]]     # 原始输出数据
    msg: Optional[str]                    # 错误消息（如果失败）
```

---

## 📂 更多示例

项目包含完整的示例代码，位于 `examples/` 目录：

- [`01_quick_start.py`](examples/01_quick_start.py) - 快速入门
- [`02_configuration.py`](examples/02_configuration.py) - 配置选项
- [`03_local_workflows.py`](examples/03_local_workflows.py) - 本地 workflow 执行
- [`04_runninghub_cloud.py`](examples/04_runninghub_cloud.py) - RunningHub 云端执行
- [`05_advanced_features.py`](examples/05_advanced_features.py) - 高级特性

运行所有示例：

```bash
cd examples
python run_all.py
```

---

## 🛠️ 开发

### 安装开发依赖

```bash
uv sync --extra dev
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
ruff check --fix
ruff format
```

---

## 🤝 贡献

欢迎贡献！请查看 [Issues](https://github.com/puke3615/ComfyKit/issues) 了解当前需要帮助的地方。

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 强大的 AI 图像生成框架
- [RunningHub](https://www.runninghub.ai) - ComfyUI 云平台

---

## 📞 联系

- 作者：Fan Wu
- Email：1129090915@qq.com
- GitHub：[@puke3615](https://github.com/puke3615)

---

<div align="center">

**如果 ComfyKit 对你有帮助，请给个 ⭐ Star！**

[GitHub](https://github.com/puke3615/ComfyKit) · [PyPI](https://pypi.org/project/comfykit/) · [问题反馈](https://github.com/puke3615/ComfyKit/issues)

</div>
