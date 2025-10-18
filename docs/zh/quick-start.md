# 快速开始

本指南将帮助你在几分钟内开始使用 ComfyKit。

## 方案一：RunningHub 云端（无需 GPU）⭐

如果你没有本地 GPU 或 ComfyUI 环境，使用 RunningHub 云平台：

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # 使用 RunningHub 初始化（只需 API key）
    kit = ComfyKit(
        runninghub_api_key="your-runninghub-key"
    )
    
    # 使用 workflow ID 执行
    result = await kit.execute("12345", {
        "prompt": "a beautiful sunset over the ocean"
    })
    
    print(f"🖼️  生成的图片: {result.images}")

asyncio.run(main())
```

!!! tip "获取 API Key"
    在 [RunningHub](https://www.runninghub.ai) 免费获取 API key

## 方案二：本地 ComfyUI

如果你有本地运行的 ComfyUI：

### 1. 启动 ComfyUI

```bash
# 启动 ComfyUI（默认端口 8188）
python main.py
```

### 2. 执行 workflow

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # 初始化（使用默认配置）
    kit = ComfyKit()
    
    # 执行 workflow
    result = await kit.execute(
        "workflow.json",
        params={"prompt": "a cute cat playing with yarn"}
    )
    
    # 检查结果
    if result.status == "completed":
        print(f"✅ 成功！耗时: {result.duration:.2f}秒")
        print(f"🖼️  图片: {result.images}")
    else:
        print(f"❌ 失败: {result.msg}")

asyncio.run(main())
```

## 理解返回结果

当你执行一个 workflow 时，ComfyKit 会返回一个 `ExecuteResult` 对象：

```python
result = await kit.execute("workflow.json", {"prompt": "a cat"})

# 基本信息
print(result.status)          # "completed" 或 "failed"
print(result.duration)        # 执行耗时（秒）
print(result.prompt_id)       # 唯一执行 ID

# 生成的媒体文件
print(result.images)          # 图片 URL 列表
print(result.videos)          # 视频 URL 列表
print(result.audios)          # 音频 URL 列表

# 按变量名分组
print(result.images_by_var)   # 按输出变量分组的图片字典
```

## 下一步

- 了解[配置选项](configuration.md)
- 探索[使用示例](usage/basic.md)
- 理解 [Workflow DSL](dsl/overview.md) 来参数化你的 workflow
- 查看完整[示例代码](examples.md)

