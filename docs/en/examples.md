# Examples

Complete example code in the `examples/` directory:

- [`01_quick_start.py`](https://github.com/puke3615/ComfyKit/blob/main/examples/01_quick_start.py) - Quick start guide
- [`02_configuration.py`](https://github.com/puke3615/ComfyKit/blob/main/examples/02_configuration.py) - Configuration options
- [`03_local_workflows.py`](https://github.com/puke3615/ComfyKit/blob/main/examples/03_local_workflows.py) - Local workflow execution
- [`04_runninghub_cloud.py`](https://github.com/puke3615/ComfyKit/blob/main/examples/04_runninghub_cloud.py) - RunningHub cloud execution
- [`05_advanced_features.py`](https://github.com/puke3615/ComfyKit/blob/main/examples/05_advanced_features.py) - Advanced features

## Run Examples

```bash
cd examples
python run_all.py
```

## Quick Example

```python
import asyncio
from comfykit import ComfyKit

async def main():
    kit = ComfyKit()
    result = await kit.execute("workflow.json", {"prompt": "a cat"})
    print(result.images)

asyncio.run(main())
```

