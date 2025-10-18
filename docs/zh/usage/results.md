# 结果处理

理解和处理 ComfyKit 的执行结果。

## ExecuteResult 对象

当你执行 workflow 时，ComfyKit 返回一个 `ExecuteResult` 对象：

```python
result = await kit.execute("workflow.json", {"prompt": "a cat"})
```

## 基本属性

### 状态

```python
# 检查执行状态
if result.status == "completed":
    print("成功！")
elif result.status == "failed":
    print(f"失败: {result.msg}")
```

### 耗时

```python
# 执行时间（秒）
print(f"执行耗时 {result.duration:.2f} 秒")
```

### Prompt ID

```python
# 唯一执行标识符
print(f"执行 ID: {result.prompt_id}")
```

## 媒体输出

### 所有媒体文件

```python
# 所有图片 URL 列表
print(result.images)  # ['http://...', 'http://...']

# 所有视频 URL 列表
print(result.videos)  # ['http://...']

# 所有音频 URL 列表
print(result.audios)  # ['http://...']

# 所有文本输出列表
print(result.texts)  # ['generated text...']
```

### 按变量名分组

如果你的 workflow 使用了 `$output.name` 标记，可以通过变量名访问输出：

```python
# 通过名称获取特定输出
cover_image = result.images_by_var["cover"][0]
thumbnail = result.images_by_var["thumbnail"][0]

# 通过名称获取视频
final_video = result.videos_by_var["final"][0]
```

## 处理图片

### 下载图片

```python
import httpx
from pathlib import Path

async def download_image(url: str, save_path: Path):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        save_path.write_bytes(response.content)

# 下载所有图片
for i, img_url in enumerate(result.images):
    await download_image(img_url, Path(f"output_{i}.png"))
```

### 在 Jupyter 中显示

```python
from IPython.display import Image, display

# 显示第一张图片
display(Image(url=result.images[0]))

# 显示所有图片
for img_url in result.images:
    display(Image(url=img_url))
```

### 使用 PIL

```python
from PIL import Image
import httpx
from io import BytesIO

async def load_pil_image(url: str) -> Image.Image:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return Image.open(BytesIO(response.content))

# 加载和处理
pil_image = await load_pil_image(result.images[0])
pil_image.show()

# 进一步处理
resized = pil_image.resize((512, 512))
resized.save("output.png")
```

## 原始输出

访问原始输出数据：

```python
# 完整的原始输出字典
print(result.outputs)
```

## 完整示例

```python
import asyncio
from comfykit import ComfyKit
from pathlib import Path
import httpx

async def main():
    kit = ComfyKit()
    
    # 执行 workflow
    result = await kit.execute("workflow.json", {
        "prompt": "a beautiful sunset"
    })
    
    # 检查状态
    if result.status != "completed":
        print(f"失败: {result.msg}")
        return
    
    print(f"✅ 成功！耗时 {result.duration:.2f}秒")
    print(f"生成了 {len(result.images)} 张图片")
    
    # 通过变量名访问
    if "cover" in result.images_by_var:
        cover_url = result.images_by_var["cover"][0]
        print(f"封面图片: {cover_url}")
    
    # 下载所有图片
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    async with httpx.AsyncClient() as client:
        for i, img_url in enumerate(result.images):
            response = await client.get(img_url)
            output_path = output_dir / f"image_{i}.png"
            output_path.write_bytes(response.content)
            print(f"已保存: {output_path}")

asyncio.run(main())
```

## 下一步

- 了解 [Workflow DSL](../dsl/overview.md) 标记输出
- 探索完整[示例](../examples.md)

