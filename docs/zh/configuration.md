# 配置

ComfyKit 配置指南。

## 配置优先级

ComfyKit 使用以下配置优先级：

1. **构造函数参数**（最高优先级）
2. **环境变量**
3. **默认值**

## 本地 ComfyUI 配置

```python
kit = ComfyKit(
    # ComfyUI 服务器 URL
    comfyui_url="http://127.0.0.1:8188",  # 默认值
    
    # 执行模式：http（推荐）或 websocket
    executor_type="http",  # 默认值
    
    # API Key（如果 ComfyUI 需要认证）
    api_key="your-api-key",
    
    # Cookies（如果需要）
    cookies="session=abc123"
)
```

## RunningHub 云端配置

```python
kit = ComfyKit(
    # RunningHub API URL
    runninghub_url="https://www.runninghub.ai",  # 默认值
    
    # RunningHub API Key（必需）
    runninghub_api_key="rh-key-xxx",
    
    # 超时（秒）
    runninghub_timeout=300,  # 默认：5 分钟
    
    # 重试次数
    runninghub_retry_count=3  # 默认：3 次重试
)
```

## 环境变量

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

## 完整示例

```python
from comfykit import ComfyKit

# 所有参数
kit = ComfyKit(
    # 本地 ComfyUI
    comfyui_url="http://127.0.0.1:8188",
    executor_type="http",
    api_key="your-api-key",
    cookies="session=abc123",
    
    # RunningHub
    runninghub_url="https://www.runninghub.ai",
    runninghub_api_key="rh-key-xxx",
    runninghub_timeout=300,
    runninghub_retry_count=3,
)
```

## 下一步

- 了解[使用方法](usage/basic.md)
- 查看 [API 参考](api-reference.md)

