# Result Processing

Understanding and processing execution results from ComfyKit.

## ExecuteResult Object

When you execute a workflow, ComfyKit returns an `ExecuteResult` object:

```python
result = await kit.execute("workflow.json", {"prompt": "a cat"})
```

## Basic Properties

### Status

```python
# Check execution status
if result.status == "completed":
    print("Success!")
elif result.status == "failed":
    print(f"Failed: {result.msg}")
```

### Duration

```python
# Execution time in seconds
print(f"Execution took {result.duration:.2f} seconds")
```

### Prompt ID

```python
# Unique execution identifier
print(f"Execution ID: {result.prompt_id}")
```

## Media Outputs

### All Media Files

```python
# List of all image URLs
print(result.images)  # ['http://...', 'http://...']

# List of all video URLs
print(result.videos)  # ['http://...']

# List of all audio URLs
print(result.audios)  # ['http://...']

# List of all text outputs
print(result.texts)  # ['generated text...']
```

### Grouped by Variable

If your workflow uses `$output.name` markers, you can access outputs by variable name:

```python
# Get specific output by name
cover_image = result.images_by_var["cover"][0]
thumbnail = result.images_by_var["thumbnail"][0]

# Get video by name
final_video = result.videos_by_var["final"][0]
```

## Processing Images

### Download Images

```python
import httpx
from pathlib import Path

async def download_image(url: str, save_path: Path):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        save_path.write_bytes(response.content)

# Download all images
for i, img_url in enumerate(result.images):
    await download_image(img_url, Path(f"output_{i}.png"))
```

### Display in Jupyter

```python
from IPython.display import Image, display

# Display first image
display(Image(url=result.images[0]))

# Display all images
for img_url in result.images:
    display(Image(url=img_url))
```

### Use with PIL

```python
from PIL import Image
import httpx
from io import BytesIO

async def load_pil_image(url: str) -> Image.Image:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return Image.open(BytesIO(response.content))

# Load and process
pil_image = await load_pil_image(result.images[0])
pil_image.show()

# Further processing
resized = pil_image.resize((512, 512))
resized.save("output.png")
```

## Raw Outputs

Access the raw output data:

```python
# Full raw output dictionary
print(result.outputs)
```

## Complete Example

```python
import asyncio
from comfykit import ComfyKit
from pathlib import Path
import httpx

async def main():
    kit = ComfyKit()
    
    # Execute workflow
    result = await kit.execute("workflow.json", {
        "prompt": "a beautiful sunset"
    })
    
    # Check status
    if result.status != "completed":
        print(f"Failed: {result.msg}")
        return
    
    print(f"✅ Success! Took {result.duration:.2f}s")
    print(f"Generated {len(result.images)} images")
    
    # Access by variable name
    if "cover" in result.images_by_var:
        cover_url = result.images_by_var["cover"][0]
        print(f"Cover image: {cover_url}")
    
    # Download all images
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    async with httpx.AsyncClient() as client:
        for i, img_url in enumerate(result.images):
            response = await client.get(img_url)
            output_path = output_dir / f"image_{i}.png"
            output_path.write_bytes(response.content)
            print(f"Saved: {output_path}")

asyncio.run(main())
```

## Next Steps

- Learn about [Workflow DSL](../dsl/overview.md) for marking outputs
- Explore complete [Examples](../examples.md)

