# RunningHub 云端执行

使用 RunningHub 云平台执行 workflow，无需本地 GPU 或 ComfyUI 安装。

## 获取 API Key

1. 访问 [RunningHub](https://www.runninghub.ai)
2. 注册免费账号
3. 从控制台获取 API key

## 基础用法

```python
from comfykit import ComfyKit

# 使用 RunningHub API key 初始化
kit = ComfyKit(
    runninghub_api_key="rh-key-xxx"
)

# 使用 workflow ID 执行
result = await kit.execute("12345", {
    "prompt": "a beautiful landscape"
})
```

## 配置选项

```python
kit = ComfyKit(
    # RunningHub API URL（可选）
    runninghub_url="https://www.runninghub.ai",  # 默认值
    
    # API Key（必需）
    runninghub_api_key="rh-key-xxx",
    
    # 超时时间（秒）（可选）
    runninghub_timeout=300,  # 默认: 5 分钟
    
    # 重试次数（可选）
    runninghub_retry_count=3  # 默认: 3 次重试
)
```

## 环境变量

```bash
export RUNNINGHUB_BASE_URL="https://www.runninghub.ai"
export RUNNINGHUB_API_KEY="rh-key-xxx"
export RUNNINGHUB_TIMEOUT="300"
export RUNNINGHUB_RETRY_COUNT="3"
```

## 完整示例

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # 使用 RunningHub 初始化
    kit = ComfyKit(
        runninghub_api_key="rh-key-xxx"
    )
    
    # 执行 workflow
    result = await kit.execute("12345", {
        "prompt": "a cute cat playing with yarn",
        "width": 1024,
        "height": 768,
        "steps": 30
    })
    
    if result.status == "completed":
        print(f"✅ 成功！耗时: {result.duration:.2f}秒")
        print(f"🖼️  图片: {result.images}")
    else:
        print(f"❌ 失败: {result.msg}")

asyncio.run(main())
```

## Workflow ID

RunningHub workflow 通过数字 ID 标识。你可以在以下位置找到 workflow ID：

- RunningHub workflow 画廊
- 你的个人 workflow 列表
- 分享的 workflow 链接

## 优势

- ☁️ **无需 GPU**：在云基础设施上运行
- 🚀 **快速**：优化的 GPU 实例
- 📦 **预配置**：所有模型和依赖已就绪
- 💰 **成本效益**：按使用量付费

## 下一步

- 了解[结果处理](results.md)
- 探索完整[示例](../examples.md)

