# Local ComfyUI

This guide covers how to use ComfyKit with a local ComfyUI installation.

## Prerequisites

1. Have ComfyUI installed locally
2. Start ComfyUI server (default port 8188)

## Starting ComfyUI

```bash
cd /path/to/ComfyUI
python main.py
```

By default, ComfyUI runs on `http://127.0.0.1:8188`.

## Basic Configuration

ComfyKit automatically connects to local ComfyUI by default:

```python
from comfykit import ComfyKit

# Uses default URL http://127.0.0.1:8188
kit = ComfyKit()
```

## Custom Configuration

If your ComfyUI runs on a different port or host:

```python
kit = ComfyKit(
    comfyui_url="http://localhost:8189"
)
```

## Executor Types

ComfyKit supports two executor types:

### HTTP Executor (Recommended)

```python
kit = ComfyKit(
    executor_type="http"  # Default
)
```

**Advantages:**
- More stable
- Better error handling
- Recommended for production

### WebSocket Executor

```python
kit = ComfyKit(
    executor_type="websocket"
)
```

**Advantages:**
- Real-time progress updates
- Lower latency for long-running workflows

## Authentication

If your ComfyUI server requires authentication:

```python
kit = ComfyKit(
    comfyui_url="http://my-server:8188",
    api_key="your-api-key",
    cookies="session=abc123"
)
```

## Environment Variables

You can also configure via environment variables:

```bash
export COMFYUI_BASE_URL="http://127.0.0.1:8188"
export COMFYUI_EXECUTOR_TYPE="http"
export COMFYUI_API_KEY="your-api-key"
export COMFYUI_COOKIES="session=abc123"
```

Then initialize without parameters:

```python
kit = ComfyKit()  # Uses environment variables
```

## Complete Example

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # Connect to local ComfyUI
    kit = ComfyKit(
        comfyui_url="http://127.0.0.1:8188",
        executor_type="http"
    )
    
    # Execute workflow
    result = await kit.execute(
        "workflow.json",
        params={
            "prompt": "a cute cat playing with yarn",
            "width": 1024,
            "height": 768
        }
    )
    
    # Check results
    if result.status == "completed":
        print(f"✅ Success! Duration: {result.duration:.2f}s")
        print(f"🖼️  Images: {result.images}")
        
        # Download images if needed
        for img_url in result.images:
            print(f"Image URL: {img_url}")
    else:
        print(f"❌ Failed: {result.msg}")

asyncio.run(main())
```

## Troubleshooting

### Connection Refused

If you get a connection refused error:

1. Make sure ComfyUI is running
2. Check the port number (default is 8188)
3. Verify the URL is correct

### Timeout Errors

For long-running workflows, you may need to increase timeout:

```python
import httpx

kit = ComfyKit(
    comfyui_url="http://127.0.0.1:8188",
)
# Note: Timeout configuration coming soon
```

## Next Steps

- Learn about [RunningHub Cloud](cloud.md) for GPU-free execution
- Understand [Result Processing](results.md)

