# 示例

`examples/` 目录中的完整示例代码：

- [`01_quick_start.py`](https://github.com/puke3615/ComfyKit/blob/main/examples/01_quick_start.py) - 快速开始指南
- [`02_configuration.py`](https://github.com/puke3615/ComfyKit/blob/main/examples/02_configuration.py) - 配置选项
- [`03_local_workflows.py`](https://github.com/puke3615/ComfyKit/blob/main/examples/03_local_workflows.py) - 本地 workflow 执行
- [`04_runninghub_cloud.py`](https://github.com/puke3615/ComfyKit/blob/main/examples/04_runninghub_cloud.py) - RunningHub 云端执行
- [`05_advanced_features.py`](https://github.com/puke3615/ComfyKit/blob/main/examples/05_advanced_features.py) - 高级特性

## 运行示例

```bash
cd examples
python run_all.py
```

## 快速示例

```python
import asyncio
from comfykit import ComfyKit

async def main():
    kit = ComfyKit()
    result = await kit.execute("workflow.json", {"prompt": "a cat"})
    print(result.images)

asyncio.run(main())
```

