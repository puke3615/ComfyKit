"""
Configuration Example - Different Ways to Configure ComfyKit

Learn how to configure ComfyKit for different scenarios.
Priority: constructor parameters > environment variables > defaults
"""

import asyncio
import os
from comfykit import ComfyKit


async def example_default():
    """Example 1: Default configuration"""
    print("\n=== Example 1: Default Configuration ===")
    
    kit = ComfyKit()
    print(f"✓ ComfyUI URL: {kit.comfyui_url}")
    print(f"✓ Executor type: {kit.executor_type}")
    
    # Verify
    assert kit.comfyui_url == "http://127.0.0.1:8188"
    assert kit.executor_type == "http"


async def example_custom_params():
    """Example 2: Custom parameters"""
    print("\n=== Example 2: Custom Parameters ===")
    
    kit = ComfyKit(
        comfyui_url="http://my-server:8188",
        executor_type="websocket",
        api_key="my-api-key"
    )
    
    print(f"✓ ComfyUI URL: {kit.comfyui_url}")
    print(f"✓ Executor type: {kit.executor_type}")
    print(f"✓ API Key: {'***' if kit.api_key else 'Not set'}")
    
    # Verify
    assert kit.comfyui_url == "http://my-server:8188"
    assert kit.api_key == "my-api-key"


async def example_env_vars():
    """Example 3: Environment variables"""
    print("\n=== Example 3: Environment Variables ===")
    
    # Set env vars (normally done in shell or .env file)
    os.environ["COMFYUI_BASE_URL"] = "http://env-server:8188"
    os.environ["COMFYUI_API_KEY"] = "env-key"
    
    kit = ComfyKit()
    print(f"✓ ComfyUI URL: {kit.comfyui_url}")
    print(f"✓ API Key: {'***' if kit.api_key else 'Not set'}")
    
    # Verify
    assert kit.comfyui_url == "http://env-server:8188"
    assert kit.api_key == "env-key"
    
    # Clean up
    del os.environ["COMFYUI_BASE_URL"]
    del os.environ["COMFYUI_API_KEY"]


async def example_priority():
    """Example 4: Configuration priority"""
    print("\n=== Example 4: Configuration Priority ===")
    
    # Set env var
    os.environ["COMFYUI_BASE_URL"] = "http://env:8188"
    
    # Param overrides env var
    kit = ComfyKit(comfyui_url="http://param:8188")
    print(f"✓ Param overrides env: {kit.comfyui_url}")
    assert kit.comfyui_url == "http://param:8188"
    
    # Clean up
    del os.environ["COMFYUI_BASE_URL"]


async def example_runninghub():
    """Example 5: RunningHub cloud configuration"""
    print("\n=== Example 5: RunningHub Cloud ===")
    
    kit = ComfyKit(
        runninghub_api_key="rh-key-xxx",
        runninghub_timeout=600
    )
    
    print(f"✓ RunningHub URL: {kit.runninghub_url}")
    print(f"✓ RunningHub timeout: {kit.runninghub_timeout}s")
    
    # Verify
    assert kit.runninghub_api_key == "rh-key-xxx"
    assert kit.runninghub_timeout == 600


async def example_multiple_instances():
    """Example 6: Multiple independent instances"""
    print("\n=== Example 6: Multiple Instances ===")
    
    kit_local = ComfyKit(comfyui_url="http://127.0.0.1:8188")
    kit_remote = ComfyKit(comfyui_url="http://remote:8188")
    
    print(f"✓ Local: {kit_local.comfyui_url}")
    print(f"✓ Remote: {kit_remote.comfyui_url}")
    
    # Verify independence
    assert kit_local.comfyui_url != kit_remote.comfyui_url


async def main():
    print("🔧 ComfyKit Configuration Examples")
    print("="*60)
    
    await example_default()
    await example_custom_params()
    await example_env_vars()
    await example_priority()
    await example_runninghub()
    await example_multiple_instances()
    
    print("\n" + "="*60)
    print("✨ All configuration examples completed!")
    print("\n📝 Key Takeaways:")
    print("  1. Simple and direct - no Config class needed")
    print("  2. Priority: params > env vars > defaults")
    print("  3. Multiple instances can have independent configs")
    print("\nNext: Check out 03_local_workflows.py for workflow execution")


if __name__ == "__main__":
    asyncio.run(main())

