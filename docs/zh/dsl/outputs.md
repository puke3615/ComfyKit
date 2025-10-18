# DSL 输出

使用 `$output.name` 标记来标记 workflow 输出，以便轻松引用生成的媒体。

## 基础输出标记

```json
{
  "9": {
    "class_type": "SaveImage",
    "_meta": {
      "title": "$output.cover"
    },
    "inputs": {
      "filename_prefix": "book_cover",
      "images": ["8", 0]
    }
  }
}
```

按名称访问：
```python
result = await kit.execute("workflow.json", params)
cover_image = result.images_by_var["cover"][0]
```

## 多个输出

```json
{
  "9": {
    "class_type": "SaveImage",
    "_meta": {
      "title": "$output.cover"
    }
  },
  "15": {
    "class_type": "SaveImage",
    "_meta": {
      "title": "$output.thumbnail"
    }
  }
}
```

分别访问：
```python
cover = result.images_by_var["cover"][0]
thumbnail = result.images_by_var["thumbnail"][0]
```

## 自动检测

没有 `$output` 标记时，ComfyKit 通过节点 ID 自动检测输出：

```python
# 通过节点 ID 访问
images_from_node_9 = result.images_by_var["9"]
```

## 下一步

- 阅读[最佳实践](best-practices.md)

