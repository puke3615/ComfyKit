# DSL Parameters

Detailed guide on parameter markers in ComfyKit's Workflow DSL.

## Basic Parameter

The simplest form - parameter name matches the field name:

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

Usage:
```python
result = await kit.execute("workflow.json", {"seed": 42})
```

## Field Mapping

Map a parameter to a different field name:

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

Usage:
```python
result = await kit.execute("workflow.json", {"prompt": "a cat"})
# "prompt" parameter maps to "text" field
```

## Required Parameters

Mark parameters as required with `!`:

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

Usage:
```python
# Must provide both width and height
result = await kit.execute("workflow.json", {
    "width": 1024,
    "height": 768
})
```

## Media Upload Parameters

Mark parameters that need file upload with `~`:

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

Usage:
```python
result = await kit.execute("workflow.json", {
    "input_image": "/path/to/image.jpg"  # Auto-uploads
})
```

## Combined Markers

Combine field mapping, upload, and required markers:

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

This means:
- Parameter name: `img`
- Maps to field: `image`
- Requires upload: `~`
- Is required: `!`

## Multiple Parameters

Define multiple parameters in one node:

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

Text without `$` is ignored (display text only).

## Optional vs Required

### Optional (with default)

```json
"_meta": {
  "title": "$seed"
}
```

- If not provided, uses default from workflow
- No error if omitted

### Required (no default)

```json
"_meta": {
  "title": "$seed!"
}
```

- Must be provided
- Errors if omitted

## Complete Example

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

Usage:
```python
result = await kit.execute("workflow.json", {
    "prompt": "a cute cat",           # Required
    "width": 1024,                     # Required
    "height": 768,                     # Required
    "model": "dreamshaper_8.safetensors",  # Optional
    "init_image": "/path/to/init.jpg"  # Optional, auto-uploads
})
```

## Next Steps

- Learn about [Outputs](outputs.md)
- Read [Best Practices](best-practices.md)

