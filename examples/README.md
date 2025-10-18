# ComfyKit Examples

Welcome to ComfyKit examples! These examples serve both as tutorials and functional tests.

## 📚 Learning Path

Follow these examples in order to learn ComfyKit:

1. **[01_quick_start.py](01_quick_start.py)** - Your first ComfyKit program
   - Simple 3-line example
   - Basic workflow execution
   - Result handling

2. **[02_configuration.py](02_configuration.py)** - Configuration options
   - Default configuration
   - Custom parameters
   - Environment variables
   - Configuration priority
   - Multiple executors

3. **[03_local_workflows.py](03_local_workflows.py)** - Local ComfyUI execution
   - Basic workflow execution
   - Custom parameters
   - Execute from dict
   - Different output types
   - Result handling

4. **[04_runninghub_cloud.py](04_runninghub_cloud.py)** - RunningHub cloud execution
   - Cloud execution basics
   - Custom configuration
   - Unified parameters
   - Auto-detection
   - Mixed local + cloud

5. **[05_advanced_features.py](05_advanced_features.py)** - Advanced features
   - Batch execution
   - Error handling
   - Timeout handling
   - Authentication
   - Executor types
   - Result processing

## 🚀 Quick Start

Run a single example:

```bash
python examples/01_quick_start.py
```

Run all examples (integration test):

```bash
python examples/run_all.py
```

## 📋 Prerequisites

### For Local Execution (examples 01, 03, 05)

- ComfyUI running at `http://127.0.0.1:8188`
- Or set `COMFYUI_BASE_URL` to your ComfyUI server

### For Cloud Execution (example 04)

- RunningHub API key
- Set environment variable:
  ```bash
  export RUNNINGHUB_API_KEY='your-api-key-here'
  ```

## 🧪 Running as Tests

All examples include assertions and can serve as integration tests:

```bash
# Run all and see summary
python examples/run_all.py

# Run specific example
python examples/02_configuration.py

# Expected failures are OK if:
# - ComfyUI is not running (local examples)
# - RUNNINGHUB_API_KEY not set (cloud examples)
# - Required workflows missing
```

## 📖 Example Structure

Each example follows this pattern:

```python
"""
Example Title - Brief Description

Detailed explanation of what this example teaches.
"""

import asyncio
from comfykit import ComfyKit


async def example_feature():
    """Specific feature demonstration"""
    kit = ComfyKit()
    result = await kit.execute(...)
    
    # Verify (acts as test)
    assert result.status == "completed"
    
    print("✅ Feature works!")


async def main():
    """Run all demonstrations"""
    await example_feature()
    print("✨ Example completed!")


if __name__ == "__main__":
    asyncio.run(main())
```

## 💡 Tips

- **Start Simple**: Begin with `01_quick_start.py`
- **Read Code**: Each example is heavily commented
- **Run & Experiment**: Modify parameters and see what happens
- **Check Errors**: Error messages guide you to solutions

## 🤝 Contributing

Found a bug or have a suggestion? Please open an issue!

Want to add an example? Follow the existing pattern and submit a PR.

## 📚 Next Steps

After completing these examples, check out:

- [README.md](../README.md) - Project documentation
- [workflows/](../workflows/) - Example workflows
- [comfykit/](../comfykit/) - Source code

Happy coding with ComfyKit! 🚀

