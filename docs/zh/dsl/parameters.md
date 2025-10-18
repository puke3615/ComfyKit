# DSL 参数

ComfyKit Workflow DSL 中参数标记的详细指南。

## 基础参数

最简单的形式 - 参数名与字段名匹配：

```json
{
  "3": {
    "class_type": "KSampler",
    "_meta": {
      "title": "$seed"
    },
    "inputs": {
      "seed": 0
    }
  }
}
```

用法：
```python
result = await kit.execute("workflow.json", {"seed": 42})
```

## 字段映射

将参数映射到不同的字段名：

```json
{
  "6": {
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "$prompt.text"
    },
    "inputs": {
      "text": "default prompt"
    }
  }
}
```

用法：
```python
result = await kit.execute("workflow.json", {"prompt": "a cat"})
# "prompt" 参数映射到 "text" 字段
```

## 必需参数

使用 `!` 标记必需参数：

```json
{
  "5": {
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "$width!, $height!"
    },
    "inputs": {
      "width": 512,
      "height": 512
    }
  }
}
```

用法：
```python
# 必须提供 width 和 height
result = await kit.execute("workflow.json", {
    "width": 1024,
    "height": 768
})
```

## 媒体上传参数

使用 `~` 标记需要文件上传的参数：

```json
{
  "10": {
    "class_type": "LoadImage",
    "_meta": {
      "title": "$~input_image"
    },
    "inputs": {
      "image": "default.png"
    }
  }
}
```

用法：
```python
result = await kit.execute("workflow.json", {
    "input_image": "/path/to/image.jpg"  # 自动上传
})
```

## 组合标记

组合字段映射、上传和必需标记：

```json
{
  "10": {
    "class_type": "LoadImage",
    "_meta": {
      "title": "$img.~image!"
    },
    "inputs": {
      "image": "default.png"
    }
  }
}
```

含义：
- 参数名：`img`
- 映射到字段：`image`
- 需要上传：`~`
- 是必需的：`!`

## 多个参数

在一个节点中定义多个参数：

```json
{
  "5": {
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Canvas Size, $width!, $height!, $batch_size"
    },
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    }
  }
}
```

不带 `$` 的文本会被忽略（仅用于显示）。

## 可选 vs 必需

### 可选（有默认值）

```json
"_meta": {
  "title": "$seed"
}
```

- 如果未提供，使用 workflow 中的默认值
- 省略时不会报错

### 必需（无默认值）

```json
"_meta": {
  "title": "$seed!"
}
```

- 必须提供
- 省略时会报错

## 完整示例

```json
{
  "4": {
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "$model.ckpt_name"
    },
    "inputs": {
      "ckpt_name": "sd_xl_base_1.0.safetensors"
    }
  },
  "5": {
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Size, $width!, $height!"
    },
    "inputs": {
      "width": 1024,
      "height": 1024
    }
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "$prompt.text!"
    },
    "inputs": {
      "text": "a beautiful landscape"
    }
  },
  "10": {
    "class_type": "LoadImage",
    "_meta": {
      "title": "$~init_image"
    },
    "inputs": {
      "image": "default.png"
    }
  }
}
```

用法：
```python
result = await kit.execute("workflow.json", {
    "prompt": "a cute cat",           # 必需
    "width": 1024,                     # 必需
    "height": 768,                     # 必需
    "model": "dreamshaper_8.safetensors",  # 可选
    "init_image": "/path/to/init.jpg"  # 可选，自动上传
})
```

## 下一步

- 了解[输出](outputs.md)
- 阅读[最佳实践](best-practices.md)

