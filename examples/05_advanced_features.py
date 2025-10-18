"""
Advanced Features Example - Batch Execution, Error Handling, and More

Learn advanced ComfyKit features for production use.
"""

import asyncio
from pathlib import Path
from comfykit import ComfyKit


async def example_batch_execution():
    """Example 1: Execute multiple workflows"""
    print("\n=== Example 1: Batch Execution ===")
    
    kit = ComfyKit()
    
    prompts = [
        "a cat",
        "a dog",
        "a bird"
    ]
    
    print(f"Executing {len(prompts)} workflows...")
    
    tasks = [
        kit.execute(
            "workflows/t2i_by_local_flux.json",
            {"prompt": prompt}
        )
        for prompt in prompts
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    success = sum(1 for r in results if not isinstance(r, Exception))
    print(f"✓ Completed: {success}/{len(prompts)}")
    
    # Verify
    assert success > 0, "At least one should succeed"


async def example_error_handling():
    """Example 2: Handle execution errors"""
    print("\n=== Example 2: Error Handling ===")
    
    kit = ComfyKit()
    
    try:
        result = await kit.execute(
            "non_existent_workflow.json",
            {"prompt": "test"}
        )
        
        if result.status == "error":
            print(f"✓ Handled error: {result.msg}")
        else:
            print(f"✓ Success: {result.status}")
            
    except FileNotFoundError as e:
        print(f"✓ Caught expected error: {e}")
    except Exception as e:
        print(f"✓ Caught error: {type(e).__name__}")


async def example_timeout_handling():
    """Example 3: Handle timeouts"""
    print("\n=== Example 3: Timeout Handling ===")
    
    kit = ComfyKit(runninghub_timeout=10)  # 10 seconds
    
    print(f"✓ Timeout set to {kit.runninghub_timeout}s")
    print("✓ Long-running tasks will timeout gracefully")


async def example_auth_configuration():
    """Example 4: Authentication"""
    print("\n=== Example 4: Authentication ===")
    
    # With API key
    kit = ComfyKit(
        api_key="your-api-key",
        cookies="session=abc123"
    )
    
    print(f"✓ API key: {'***' if kit.api_key else 'None'}")
    print(f"✓ Cookies: {'***' if kit.cookies else 'None'}")
    print("✓ Authentication configured")


async def example_executor_types():
    """Example 5: Different executor types"""
    print("\n=== Example 5: Executor Types ===")
    
    # HTTP (default, recommended)
    http_kit = ComfyKit(executor_type="http")
    print(f"✓ HTTP mode: {http_kit.executor_type}")
    
    # WebSocket (for long-running tasks)
    ws_kit = ComfyKit(executor_type="websocket")
    print(f"✓ WebSocket mode: {ws_kit.executor_type}")
    
    # Verify
    assert http_kit.executor_type == "http"
    assert ws_kit.executor_type == "websocket"


async def example_result_processing():
    """Example 6: Process results"""
    print("\n=== Example 6: Result Processing ===")
    
    kit = ComfyKit()
    
    result = await kit.execute(
        "workflows/t2i_by_local_flux.json",
        {"prompt": "a test image"}
    )
    
    # Different ways to access results
    print(f"✓ Status: {result.status}")
    print(f"✓ Duration: {result.duration}s")
    print(f"✓ Prompt ID: {result.prompt_id}")
    
    # All images (flat list)
    print(f"✓ Total images: {len(result.images)}")
    
    # Images by variable name
    for var_name, images in result.images_by_var.items():
        print(f"✓ Variable '{var_name}': {len(images)} images")
    
    # Check different output types
    if result.videos:
        print(f"✓ Videos: {len(result.videos)}")
    if result.audios:
        print(f"✓ Audios: {len(result.audios)}")
    if result.texts:
        print(f"✓ Texts: {len(result.texts)}")


async def example_workflow_from_path():
    """Example 7: Different workflow sources"""
    print("\n=== Example 7: Workflow Sources ===")
    
    kit = ComfyKit()
    
    # From string path
    result1 = await kit.execute("workflows/t2i_by_local_flux.json")
    print(f"✓ From string path: {result1.status}")
    
    # From Path object
    result2 = await kit.execute(
        Path("workflows/t2i_by_local_flux.json")
    )
    print(f"✓ From Path object: {result2.status}")
    
    # From URL (downloads automatically)
    # result3 = await kit.execute("https://example.com/workflow.json")
    # print(f"✓ From URL: {result3.status}")
    
    # From RunningHub ID
    # result4 = await kit.execute("12345")
    # print(f"✓ From RunningHub ID: {result4.status}")


async def main():
    print("🚀 ComfyKit Advanced Features Examples")
    print("="*60)
    print("\n💡 These examples show production-ready features\n")
    
    try:
        await example_batch_execution()
        await example_error_handling()
        await example_timeout_handling()
        await example_auth_configuration()
        await example_executor_types()
        await example_result_processing()
        await example_workflow_from_path()
        
        print("\n" + "="*60)
        print("✨ All advanced examples completed!")
        print("\n📝 Key Takeaways:")
        print("  1. Batch execution with asyncio.gather()")
        print("  2. Graceful error handling")
        print("  3. Flexible authentication options")
        print("  4. Multiple executor types available")
        print("  5. Rich result processing")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Some examples require a running ComfyUI server")


if __name__ == "__main__":
    asyncio.run(main())

