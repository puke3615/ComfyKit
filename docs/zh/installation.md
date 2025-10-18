# 安装

## 系统要求

- Python 3.10 或更高版本
- pip 或 uv 包管理器

## 使用 pip 安装

```bash
pip install comfykit
```

## 使用 uv 安装（推荐）

```bash
uv add comfykit
```

## 验证安装

```python
from comfykit import ComfyKit

print("ComfyKit 安装成功！")
```

## 可选依赖

### 开发依赖

如果你想为 ComfyKit 贡献代码，安装开发依赖：

```bash
pip install comfykit[dev]
```

或使用 uv：

```bash
uv sync --extra dev
```

包含以下工具：
- pytest - 测试框架
- pytest-asyncio - 异步测试支持
- black - 代码格式化
- ruff - 代码检查

## 下一步

安装完成后，查看[快速开始](quick-start.md)指南开始使用 ComfyKit。

