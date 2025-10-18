# 开发

ComfyKit 开发指南。

## 安装开发依赖

```bash
uv sync --extra dev
```

## 运行测试

```bash
pytest
```

## 代码格式化

```bash
ruff check --fix
ruff format
```

## 项目结构

```
ComfyKit/
├── comfykit/           # 主包
│   ├── comfyui/        # ComfyUI 集成
│   └── utils/          # 工具函数
├── examples/           # 示例脚本
├── workflows/          # 示例 workflow
└── tests/              # 测试套件
```

## 下一步

- 查看[贡献指南](contributing.md)
- 阅读 [API 参考](api-reference.md)

