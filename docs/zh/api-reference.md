# API 参考

ComfyKit 完整 API 参考。

## ComfyKit 类

### 构造函数

```python
class ComfyKit:
    def __init__(
        self,
        # 本地 ComfyUI 配置
        comfyui_url: Optional[str] = None,
        executor_type: Literal["http", "websocket"] = "http",
        api_key: Optional[str] = None,
        cookies: Optional[str] = None,
        
        # RunningHub 云端配置
        runninghub_url: Optional[str] = None,
        runninghub_api_key: Optional[str] = None,
        runninghub_timeout: int = 300,
        runninghub_retry_count: int = 3,
    )
```

### execute 方法

```python
async def execute(
    self,
    workflow: Union[str, Path],
    params: Optional[Dict[str, Any]] = None,
) -> ExecuteResult
```

**参数：**
- `workflow`: Workflow 源（文件路径、URL 或 RunningHub ID）
- `params`: Workflow 参数

**返回：**
- `ExecuteResult`: 结构化执行结果

### execute_json 方法

```python
async def execute_json(
    self,
    workflow_json: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None,
) -> ExecuteResult
```

**参数：**
- `workflow_json`: Workflow JSON 字典
- `params`: Workflow 参数

**返回：**
- `ExecuteResult`: 结构化执行结果

## ExecuteResult 类

```python
class ExecuteResult:
    status: str                           # "completed" 或 "failed"
    prompt_id: Optional[str]              # Prompt ID
    duration: Optional[float]             # 执行时间（秒）
    
    # 媒体输出
    images: List[str]                     # 所有图片 URL
    videos: List[str]                     # 所有视频 URL
    audios: List[str]                     # 所有音频 URL
    texts: List[str]                      # 所有文本输出
    
    # 按变量名分组
    images_by_var: Dict[str, List[str]]   # 按变量分组的图片
    videos_by_var: Dict[str, List[str]]   # 按变量分组的视频
    audios_by_var: Dict[str, List[str]]   # 按变量分组的音频
    texts_by_var: Dict[str, List[str]]    # 按变量分组的文本
    
    # 原始输出
    outputs: Optional[Dict[str, Any]]     # 原始输出数据
    msg: Optional[str]                    # 错误消息（如果失败）
```

## 使用示例

```python
import asyncio
from comfykit import ComfyKit

async def main():
    # 初始化
    kit = ComfyKit()
    
    # 执行 workflow
    result = await kit.execute("workflow.json", {
        "prompt": "a cute cat"
    })
    
    # 访问结果
    print(f"状态: {result.status}")
    print(f"图片: {result.images}")
    print(f"耗时: {result.duration}秒")

asyncio.run(main())
```

## 下一步

- 查看完整[示例](examples.md)
- 了解[配置](configuration.md)

