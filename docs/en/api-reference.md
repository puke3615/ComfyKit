# API Reference

Complete API reference for ComfyKit.

## ComfyKit Class

### Constructor

```python
class ComfyKit:
    def __init__(
        self,
        # Local ComfyUI configuration
        comfyui_url: Optional[str] = None,
        executor_type: Literal["http", "websocket"] = "http",
        api_key: Optional[str] = None,
        cookies: Optional[str] = None,
        
        # RunningHub cloud configuration
        runninghub_url: Optional[str] = None,
        runninghub_api_key: Optional[str] = None,
        runninghub_timeout: int = 300,
        runninghub_retry_count: int = 3,
    )
```

### execute Method

```python
async def execute(
    self,
    workflow: Union[str, Path],
    params: Optional[Dict[str, Any]] = None,
) -> ExecuteResult
```

**Parameters:**
- `workflow`: Workflow source (file path, URL, or RunningHub ID)
- `params`: Workflow parameters

**Returns:**
- `ExecuteResult`: Structured execution result

### execute_json Method

```python
async def execute_json(
    self,
    workflow_json: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None,
) -> ExecuteResult
```

**Parameters:**
- `workflow_json`: Workflow JSON dictionary
- `params`: Workflow parameters

**Returns:**
- `ExecuteResult`: Structured execution result

## ExecuteResult Class

```python
class ExecuteResult:
    status: str                           # "completed" or "failed"
    prompt_id: Optional[str]              # Prompt ID
    duration: Optional[float]             # Duration in seconds
    
    # Media outputs
    images: List[str]                     # All image URLs
    videos: List[str]                     # All video URLs
    audios: List[str]                     # All audio URLs
    texts: List[str]                      # All text outputs
    
    # Grouped by variable name
    images_by_var: Dict[str, List[str]]   # Images by variable
    videos_by_var: Dict[str, List[str]]   # Videos by variable
    audios_by_var: Dict[str, List[str]]   # Audios by variable
    texts_by_var: Dict[str, List[str]]    # Texts by variable
    
    # Raw outputs
    outputs: Optional[Dict[str, Any]]     # Raw output data
    msg: Optional[str]                    # Error message (if failed)
```

## Usage Example

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # Initialize
    kit = ComfyKit()
    
    # Execute workflow
    result = await kit.execute("workflow.json", {
        "prompt": "a cute cat"
    })
    
    # Access results
    print(f"Status: {result.status}")
    print(f"Images: {result.images}")
    print(f"Duration: {result.duration}s")

asyncio.run(main())
```

## Next Steps

- Check out complete [Examples](examples.md)
- Learn about [Configuration](configuration.md)

