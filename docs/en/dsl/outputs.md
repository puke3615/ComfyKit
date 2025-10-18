# DSL Outputs

Mark workflow outputs with the `$output.name` marker to easily reference generated media.

## Basic Output Marking

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

Access by name:
```python
result = await kit.execute("workflow.json", params)
cover_image = result.images_by_var["cover"][0]
```

## Multiple Outputs

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

Access each:
```python
cover = result.images_by_var["cover"][0]
thumbnail = result.images_by_var["thumbnail"][0]
```

## Auto-detection

Without `$output` markers, ComfyKit auto-detects outputs by node ID:

```python
# Access by node ID
images_from_node_9 = result.images_by_var["9"]
```

## Next Steps

- Read [Best Practices](best-practices.md)

