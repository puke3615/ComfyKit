# 本地 ComfyUI

本指南介绍如何使用 ComfyKit 连接本地 ComfyUI。

## 前置条件

1. 已安装 ComfyUI
2. 启动 ComfyUI 服务器（默认端口 8188）

## 启动 ComfyUI

```bash
cd /path/to/ComfyUI
python main.py
```

默认情况下，ComfyUI 运行在 `http://127.0.0.1:8188`。

## 基础配置

ComfyKit 默认自动连接本地 ComfyUI：

```python
from comfykit import ComfyKit

# 使用默认 URL http://127.0.0.1:8188
kit = ComfyKit()
```

## 自定义配置

如果你的 ComfyUI 运行在不同的端口或主机：

```python
kit = ComfyKit(
    comfyui_url="http://localhost:8189"
)
```

## 执行器类型

ComfyKit 支持两种执行器类型：

### HTTP 执行器（推荐）

```python
kit = ComfyKit(
    executor_type="http"  # 默认
)
```

**优点：**
- 更稳定
- 更好的错误处理
- 生产环境推荐

### WebSocket 执行器

```python
kit = ComfyKit(
    executor_type="websocket"
)
```

**优点：**
- 实时进度更新
- 长时间运行的 workflow 延迟更低

## 认证

如果你的 ComfyUI 服务器需要认证：

```python
kit = ComfyKit(
    comfyui_url="http://my-server:8188",
    api_key="your-api-key",
    cookies="session=abc123"
)
```

## 环境变量

你也可以通过环境变量配置：

```bash
export COMFYUI_BASE_URL="http://127.0.0.1:8188"
export COMFYUI_EXECUTOR_TYPE="http"
export COMFYUI_API_KEY="your-api-key"
export COMFYUI_COOKIES="session=abc123"
```

然后无参数初始化：

```python
kit = ComfyKit()  # 使用环境变量
```

## 完整示例

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # 连接本地 ComfyUI
    kit = ComfyKit(
        comfyui_url="http://127.0.0.1:8188",
        executor_type="http"
    )
    
    # 执行 workflow
    result = await kit.execute(
        "workflow.json",
        params={
            "prompt": "a cute cat playing with yarn",
            "width": 1024,
            "height": 768
        }
    )
    
    # 检查结果
    if result.status == "completed":
        print(f"✅ 成功！耗时: {result.duration:.2f}秒")
        print(f"🖼️  图片: {result.images}")
        
        # 如需要可以下载图片
        for img_url in result.images:
            print(f"图片 URL: {img_url}")
    else:
        print(f"❌ 失败: {result.msg}")

asyncio.run(main())
```

## 故障排查

### 连接被拒绝

如果遇到连接被拒绝错误：

1. 确保 ComfyUI 正在运行
2. 检查端口号（默认是 8188）
3. 验证 URL 是否正确

### 超时错误

对于长时间运行的 workflow，可能需要增加超时时间：

```python
import httpx

kit = ComfyKit(
    comfyui_url="http://127.0.0.1:8188",
)
# 注意：超时配置即将推出
```

## 下一步

- 了解 [RunningHub 云端](cloud.md) 无需 GPU 执行
- 理解[结果处理](results.md)

