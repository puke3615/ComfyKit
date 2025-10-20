# Quick Start

This guide will help you get started with ComfyKit in minutes.

## Option 1: RunningHub Cloud (No GPU needed) ⭐

If you don't have a local GPU or ComfyUI environment, use RunningHub cloud:

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # Initialize with RunningHub (only API key needed)
    kit = ComfyKit(
        runninghub_api_key="your-runninghub-key"
    )
    
    # Execute with workflow ID
    result = await kit.execute("12345", {
        "prompt": "a beautiful sunset over the ocean"
    })
    
    print(f"🖼️  Generated images: {result.images}")

asyncio.run(main())
```

!!! tip "Get Your API Key"
    Get your free API key at [RunningHub](https://www.runninghub.ai)

## Option 2: Local ComfyUI

If you have ComfyUI running locally:

### 1. Start ComfyUI

```bash
# Start ComfyUI (default port 8188)
python main.py
```

### 2. Execute workflow

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # Connect to local ComfyUI (default: http://127.0.0.1:8188)
    kit = ComfyKit(comfyui_url="http://127.0.0.1:8188")
    
    # Execute workflow
    result = await kit.execute(
        "workflow.json",
        params={"prompt": "a cute cat playing with yarn"}
    )
    
    # Check results
    if result.status == "completed":
        print(f"✅ Success! Duration: {result.duration:.2f}s")
        print(f"🖼️  Images: {result.images}")
    else:
        print(f"❌ Failed: {result.msg}")

asyncio.run(main())
```

> 💡 **Tip**: `comfyui_url` defaults to `http://127.0.0.1:8188` and can be omitted

## Understanding the Results

When you execute a workflow, ComfyKit returns an `ExecuteResult` object:

```python
result = await kit.execute("workflow.json", {"prompt": "a cat"})

# Basic information
print(result.status)          # "completed" or "failed"
print(result.duration)        # Execution time in seconds
print(result.prompt_id)       # Unique execution ID

# Generated media
print(result.images)          # List of image URLs
print(result.videos)          # List of video URLs
print(result.audios)          # List of audio URLs

# Grouped by variable name
print(result.images_by_var)   # Dict of images grouped by output variable
```

## Next Steps

- Learn about [Configuration](configuration.md) options
- Explore [Usage Examples](usage/basic.md)
- Understand [Workflow DSL](dsl/overview.md) for parameterizing workflows
- Check out complete [Examples](examples.md)

