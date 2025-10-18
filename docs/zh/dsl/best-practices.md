# DSL 最佳实践

有效使用 ComfyKit Workflow DSL 的指南。

## 参数命名

✅ **好**: 使用描述性名称
```json
"_meta": {"title": "$positive_prompt.text!"}
```

❌ **不好**: 使用单字母
```json
"_meta": {"title": "$p.text!"}
```

## 必需标记

对没有合理默认值的参数使用 `!`：

✅ **好**: Prompt 是必需的
```json
"_meta": {"title": "$prompt.text!"}
```

❌ **不好**: Seed 通常有好的默认值
```json
"_meta": {"title": "$seed!"}
```

## 上传标记

总是对图片/视频/音频参数使用 `~`：

✅ **好**:
```json
"_meta": {"title": "$~input_image"}
```

## 输出变量

对重要输出使用 `$output.xxx`：

✅ **好**: 命名的输出易于引用
```json
"_meta": {"title": "$output.final_image"}
```

## 显示文本

添加描述性文本以提高清晰度：

✅ **好**:
```json
"_meta": {"title": "Canvas Size, $width!, $height!"}
```

❌ **不好**:
```json
"_meta": {"title": "$width!, $height!"}
```

## 完整示例

```json
{
  "5": {
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Canvas, $width!, $height!"
    }
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "$positive_prompt.text!"
    }
  },
  "10": {
    "class_type": "LoadImage",
    "_meta": {
      "title": "$~init_image"
    }
  },
  "9": {
    "class_type": "SaveImage",
    "_meta": {
      "title": "$output.final"
    }
  }
}
```

