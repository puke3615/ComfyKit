# Workflow DSL 概览

ComfyKit 提供了简洁的 DSL（领域特定语言）来标记 workflow 节点，允许你：

- 定义动态参数
- 标记输出变量
- 指定必需/可选参数
- 自动处理媒体文件上传

## DSL 语法快速参考

这些 DSL 标记写在 **ComfyUI workflow 节点的 title 字段**中，用于将固定的 workflow 转换为可参数化的模板。

**使用步骤**：
1. 在 ComfyUI 编辑器中双击节点，修改 title 添加 DSL 标记（如 `$prompt.text!`）
2. 保存为 **API 格式 JSON**（菜单选择 "Save (API Format)"，不是普通 "Save"）
3. 通过 `kit.execute("workflow.json", {"prompt": "value"})` 传参执行

> ⚠️ **注意**：必须使用 API 格式的 workflow JSON，不是 UI 格式。

| 语法 | 描述 | 示例 | 效果 |
|--------|-------------|---------|--------|
| `$param` | 基础参数（简写） | `$prompt` | 参数 `prompt`，映射到字段 `prompt` |
| `$param.field` | 指定字段映射 | `$prompt.text` | 参数 `prompt`，映射到字段 `text` |
| `$param!` | 必需参数 | `$prompt!` | 参数 `prompt` 是必需的，无默认值 |
| `$~param` | 媒体参数（上传） | `$~image` | 参数 `image` 需要文件上传 |
| `$~param!` | 必需媒体参数 | `$~image!` | 参数 `image` 是必需的且需要上传 |
| `$param.~field!` | 组合标记 | `$img.~image!` | 参数 `img` 映射到 `image`，必需且上传 |
| `$output.name` | 输出变量标记 | `$output.cover` | 标记输出变量名为 `cover` |
| `Text, $p1, $p2` | 多个参数 | `Size, $width!, $height!` | 在一个节点中定义多个参数 |

## 工作原理

DSL 通过在 workflow 节点的 `_meta.title` 字段添加标记来工作：

```json
{
  "6": {
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "$prompt.text!"
    },
    "inputs": {
      "text": "a beautiful landscape",
      "clip": ["4", 1]
    }
  }
}
```

当你执行这个 workflow：

```python
result = await kit.execute("workflow.json", {
    "prompt": "a cute cat"
})
```

ComfyKit 会自动：
1. 解析 DSL 标记
2. 将 `text` 字段替换为 "a cute cat"
3. 执行修改后的 workflow

## 标记类型

### 参数标记

- `$param` - 基础参数
- `$param.field` - 带字段映射的参数
- `$param!` - 必需参数
- `$~param` - 媒体上传参数

详见[参数](parameters.md)详细示例。

### 输出标记

- `$output.name` - 标记输出变量

详见[输出](outputs.md)详细示例。

## 下一步

- 详细了解[参数](parameters.md)
- 理解[输出](outputs.md)标记
- 阅读[最佳实践](best-practices.md)

