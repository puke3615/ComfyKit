# Workflow DSL Overview

ComfyKit provides a concise DSL (Domain Specific Language) for marking workflow nodes, allowing you to:

- Define dynamic parameters
- Mark output variables
- Specify required/optional parameters
- Automatically handle media file uploads

## DSL Syntax Quick Reference

These DSL markers are written in the **title field of ComfyUI workflow nodes** to convert fixed workflows into parameterizable templates.

**Usage Steps**:
1. In ComfyUI editor, double-click a node and modify its title to add DSL markers (e.g., `$prompt.text!`)
2. Save as **API format JSON** (select "Save (API Format)" from menu, not regular "Save")
3. Execute with parameters via `kit.execute("workflow.json", {"prompt": "value"})`

> ⚠️ **Important**: ComfyKit requires API format workflow JSON, not UI format.

| Syntax | Description | Example | Effect |
|--------|-------------|---------|--------|
| `$param` | Basic parameter (shorthand) | `$prompt` | Parameter `prompt`, maps to field `prompt` |
| `$param.field` | Specify field mapping | `$prompt.text` | Parameter `prompt`, maps to field `text` |
| `$param!` | Required parameter | `$prompt!` | Parameter `prompt` is required, no default |
| `$~param` | Media parameter (upload) | `$~image` | Parameter `image` requires file upload |
| `$~param!` | Required media parameter | `$~image!` | Parameter `image` is required and needs upload |
| `$param.~field!` | Combined markers | `$img.~image!` | Parameter `img` maps to `image`, required and upload |
| `$output.name` | Output variable marker | `$output.cover` | Mark output variable name as `cover` |
| `Text, $p1, $p2` | Multiple parameters | `Size, $width!, $height!` | Define multiple parameters in one node |

## How It Works

The DSL works by adding markers to the `_meta.title` field of workflow nodes:

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

When you execute this workflow:

```python
result = await kit.execute("workflow.json", {
    "prompt": "a cute cat"
})
```

ComfyKit automatically:
1. Parses the DSL markers
2. Replaces the `text` field with "a cute cat"
3. Executes the modified workflow

## Marker Types

### Parameter Markers

- `$param` - Basic parameter
- `$param.field` - Parameter with field mapping
- `$param!` - Required parameter
- `$~param` - Media upload parameter

See [Parameters](parameters.md) for detailed examples.

### Output Markers

- `$output.name` - Mark output variables

See [Outputs](outputs.md) for detailed examples.

## Next Steps

- Learn about [Parameters](parameters.md) in detail
- Understand [Outputs](outputs.md) marking
- Read [Best Practices](best-practices.md)

