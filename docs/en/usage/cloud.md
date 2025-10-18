# RunningHub Cloud Execution

Use RunningHub cloud platform to execute workflows without local GPU or ComfyUI installation.

## Get API Key

1. Visit [RunningHub](https://www.runninghub.ai)
2. Sign up for a free account
3. Get your API key from the dashboard

## Basic Usage

```python
from comfykit import ComfyKit

# Initialize with RunningHub API key
kit = ComfyKit(
    runninghub_api_key="rh-key-xxx"
)

# Execute with workflow ID
result = await kit.execute("12345", {
    "prompt": "a beautiful landscape"
})
```

## Configuration

```python
kit = ComfyKit(
    # RunningHub API URL (optional)
    runninghub_url="https://www.runninghub.ai",  # Default
    
    # API Key (required)
    runninghub_api_key="rh-key-xxx",
    
    # Timeout in seconds (optional)
    runninghub_timeout=300,  # Default: 5 minutes
    
    # Retry count (optional)
    runninghub_retry_count=3  # Default: 3 retries
)
```

## Environment Variables

```bash
export RUNNINGHUB_BASE_URL="https://www.runninghub.ai"
export RUNNINGHUB_API_KEY="rh-key-xxx"
export RUNNINGHUB_TIMEOUT="300"
export RUNNINGHUB_RETRY_COUNT="3"
```

## Complete Example

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # Initialize with RunningHub
    kit = ComfyKit(
        runninghub_api_key="rh-key-xxx"
    )
    
    # Execute workflow
    result = await kit.execute("12345", {
        "prompt": "a cute cat playing with yarn",
        "width": 1024,
        "height": 768,
        "steps": 30
    })
    
    if result.status == "completed":
        print(f"✅ Success! Duration: {result.duration:.2f}s")
        print(f"🖼️  Images: {result.images}")
    else:
        print(f"❌ Failed: {result.msg}")

asyncio.run(main())
```

## Workflow IDs

RunningHub workflows are identified by numeric IDs. You can find workflow IDs in:

- RunningHub workflow gallery
- Your personal workflow list
- Shared workflow links

## Advantages

- ☁️ **No GPU Required**: Run on cloud infrastructure
- 🚀 **Fast**: Optimized GPU instances
- 📦 **Pre-configured**: All models and dependencies ready
- 💰 **Cost-effective**: Pay only for what you use

## Next Steps

- Learn about [Result Processing](results.md)
- Explore complete [Examples](../examples.md)

