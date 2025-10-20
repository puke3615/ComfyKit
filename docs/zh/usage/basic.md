# 基础用法

## 执行本地 Workflow

最基本的用法是执行本地 workflow 文件：

```python
from comfykit import ComfyKit

# Connect to local ComfyUI (default: http://127.0.0.1:8188)
kit = ComfyKit()

# 执行本地 workflow 文件
result = await kit.execute("workflow.json", {
    "prompt": "a cat",
    "seed": 42,
    "steps": 20
})
```

## 执行远程 Workflow URL

ComfyKit 可以自动下载并执行来自 URL 的 workflow：

```python
# 自动下载并执行
result = await kit.execute(
    "https://example.com/workflow.json",
    {"prompt": "a cat"}
)
```

## 从字典执行 Workflow

你也可以将 workflow 作为 Python 字典传递：

```python
workflow_dict = {
    "nodes": [...],
    "edges": [...]
}

result = await kit.execute_json(workflow_dict, {
    "prompt": "a cat"
})
```

## 自定义 ComfyUI 服务器

连接到远程 ComfyUI 服务器：

```python
kit = ComfyKit(
    comfyui_url="http://my-server:8188",
    api_key="your-api-key"  # 如果需要认证
)
```

## 参数

Workflows 可以接受在 workflow DSL 中定义的参数。详见 [Workflow DSL](../dsl/overview.md)。

```python
result = await kit.execute("workflow.json", {
    "prompt": "a beautiful landscape",
    "width": 1024,
    "height": 768,
    "seed": 42,
    "steps": 30
})
```

## 错误处理

始终检查执行状态：

```python
result = await kit.execute("workflow.json", params)

if result.status == "completed":
    print("成功！")
    print(f"图片: {result.images}")
else:
    print(f"失败: {result.msg}")
```

## Async/Await

ComfyKit 的所有操作都使用 async/await：

```python
import asyncio
from comfykit import ComfyKit

async def main():
    kit = ComfyKit()
    result = await kit.execute("workflow.json", {"prompt": "a cat"})
    print(result.images)

# 运行异步函数
asyncio.run(main())
```

## 下一步

- 了解[本地 ComfyUI](local.md) 设置
- 探索 [RunningHub 云端](cloud.md) 执行
- 理解[结果处理](results.md)

