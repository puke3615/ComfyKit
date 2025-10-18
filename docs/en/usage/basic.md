# Basic Usage

## Execute Local Workflow

The most basic usage is to execute a local workflow file:

```python
from comfykit import ComfyKit

kit = ComfyKit()

# Execute local workflow file
result = await kit.execute("workflow.json", {
    "prompt": "a cat",
    "seed": 42,
    "steps": 20
})
```

## Execute Remote Workflow URL

ComfyKit can automatically download and execute workflows from URLs:

```python
# Automatically download and execute
result = await kit.execute(
    "https://example.com/workflow.json",
    {"prompt": "a cat"}
)
```

## Execute Workflow from Dict

You can also pass a workflow as a Python dictionary:

```python
workflow_dict = {
    "nodes": [...],
    "edges": [...]
}

result = await kit.execute_json(workflow_dict, {
    "prompt": "a cat"
})
```

## Custom ComfyUI Server

Connect to a remote ComfyUI server:

```python
kit = ComfyKit(
    comfyui_url="http://my-server:8188",
    api_key="your-api-key"  # If authentication is required
)
```

## Parameters

Workflows can accept parameters that are defined in the workflow DSL. See [Workflow DSL](../dsl/overview.md) for more details.

```python
result = await kit.execute("workflow.json", {
    "prompt": "a beautiful landscape",
    "width": 1024,
    "height": 768,
    "seed": 42,
    "steps": 30
})
```

## Error Handling

Always check the execution status:

```python
result = await kit.execute("workflow.json", params)

if result.status == "completed":
    print("Success!")
    print(f"Images: {result.images}")
else:
    print(f"Failed: {result.msg}")
```

## Async/Await

ComfyKit uses async/await for all operations:

```python
import asyncio
from comfykit import ComfyKit

async def main():
    kit = ComfyKit()
    result = await kit.execute("workflow.json", {"prompt": "a cat"})
    print(result.images)

# Run the async function
asyncio.run(main())
```

## Next Steps

- Learn about [Local ComfyUI](local.md) setup
- Explore [RunningHub Cloud](cloud.md) execution
- Understand [Result Processing](results.md)

