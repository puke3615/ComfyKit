# DSL Best Practices

Guidelines for using ComfyKit's Workflow DSL effectively.

## Parameter Naming

✅ **Good**: Use descriptive names
```json
"_meta": {"title": "$positive_prompt.text!"}
```

❌ **Bad**: Use single letters
```json
"_meta": {"title": "$p.text!"}
```

## Required Markers

Use `!` for parameters with no reasonable default:

✅ **Good**: Prompt is required
```json
"_meta": {"title": "$prompt.text!"}
```

❌ **Bad**: Seed probably has a good default
```json
"_meta": {"title": "$seed!"}
```

## Upload Markers

Always use `~` for image/video/audio parameters:

✅ **Good**:
```json
"_meta": {"title": "$~input_image"}
```

## Output Variables

Use `$output.xxx` for important outputs:

✅ **Good**: Named outputs are easy to reference
```json
"_meta": {"title": "$output.final_image"}
```

## Display Text

Add descriptive text for clarity:

✅ **Good**:
```json
"_meta": {"title": "Canvas Size, $width!, $height!"}
```

❌ **Bad**:
```json
"_meta": {"title": "$width!, $height!"}
```

## Complete Example

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

