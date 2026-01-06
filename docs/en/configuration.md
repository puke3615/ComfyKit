# Configuration

ComfyKit configuration guide.

## Configuration Priority

ComfyKit uses the following priority for configuration:

1. **Constructor parameters** (highest priority)
2. **Environment variables**
3. **Default values**

## Local ComfyUI Configuration

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

## RunningHub Cloud Configuration

```python
kit = ComfyKit(
    # RunningHub API URL
    runninghub_url="https://www.runninghub.ai",  # Default
    
    # RunningHub API Key (required)
    runninghub_api_key="rh-key-xxx",
    
    # Timeout (seconds)
    runninghub_timeout=300,  # Default: 5 minutes
    
    # Retry count
    runninghub_retry_count=3,  # Default: 3 retries
    
    # Instance type (optional)
    runninghub_instance_type="plus"  # Use 48GB VRAM machine
)
```

## Environment Variables

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
export RUNNINGHUB_INSTANCE_TYPE="plus"  # Optional, use 48GB VRAM machine
```

## Complete Example

```python
from comfykit import ComfyKit

# All parameters
kit = ComfyKit(
    # Local ComfyUI
    comfyui_url="http://127.0.0.1:8188",
    executor_type="http",
    api_key="your-api-key",
    cookies="session=abc123",
    
    # RunningHub
    runninghub_url="https://www.runninghub.ai",
    runninghub_api_key="rh-key-xxx",
    runninghub_timeout=300,
    runninghub_retry_count=3,
    runninghub_instance_type="plus",  # Optional, use 48GB VRAM machine
)
```

## Next Steps

- Learn about [Usage](usage/basic.md)
- Check [API Reference](api-reference.md)

