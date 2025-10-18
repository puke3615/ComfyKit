"""
RunningHub Cloud Example - Execute Workflows on RunningHub

Learn how to use RunningHub cloud platform for workflow execution.
No local ComfyUI needed!
"""

import asyncio
import os
from comfykit import ComfyKit


async def example_basic_cloud():
    """Example 1: Basic RunningHub execution"""
    print("\n=== Example 1: Basic Cloud Execution ===")
    
    # Check API key
    if not os.getenv("RUNNINGHUB_API_KEY"):
        print("⚠️  RUNNINGHUB_API_KEY not set, skipping example")
        print("   Set it with: export RUNNINGHUB_API_KEY='your-key'")
        return False
    
    kit = ComfyKit()
    
    # Execute with workflow ID (numeric string)
    result = await kit.execute(
        "12345",  # RunningHub workflow ID
        {"prompt": "a beautiful sunset"}
    )
    
    print(f"✓ Status: {result.status}")
    print(f"✓ Images: {len(result.images)}")
    
    # Verify
    assert result.status == "completed"
    return True


async def example_with_config():
    """Example 2: RunningHub with custom config"""
    print("\n=== Example 2: Custom Configuration ===")
    
    api_key = os.getenv("RUNNINGHUB_API_KEY")
    if not api_key:
        print("⚠️  Skipped (no API key)")
        return False
    
    kit = ComfyKit(
        runninghub_api_key=api_key,
        runninghub_timeout=600,  # 10 minutes
        runninghub_retry_count=5
    )
    
    result = await kit.execute(
        "12345",
        {"prompt": "a cyberpunk city", "seed": 42}
    )
    
    print(f"✓ Status: {result.status}")
    print(f"✓ Timeout: {kit.runninghub_timeout}s")
    return True


async def example_same_params_format():
    """Example 3: Same parameter format as local"""
    print("\n=== Example 3: Unified Parameters ===")
    
    if not os.getenv("RUNNINGHUB_API_KEY"):
        print("⚠️  Skipped (no API key)")
        return False
    
    kit = ComfyKit()
    
    # Same simple format works for both local and cloud!
    params = {
        "prompt": "a test prompt",
        "seed": 42,
        "steps": 20
    }
    
    # ComfyKit handles the conversion automatically
    result = await kit.execute("12345", params)
    
    print(f"✓ Same params format for local and cloud")
    print(f"✓ Status: {result.status}")
    return True


async def example_auto_detection():
    """Example 4: Automatic workflow type detection"""
    print("\n=== Example 4: Auto-Detection ===")
    
    if not os.getenv("RUNNINGHUB_API_KEY"):
        print("⚠️  Skipped (no API key)")
        return False
    
    kit = ComfyKit()
    
    # ComfyKit auto-detects:
    # - "12345" → RunningHub (numeric)
    # - "workflow.json" → Local file
    # - "https://..." → Download and execute
    
    result = await kit.execute("12345", {"prompt": "auto"})
    print(f"✓ Auto-detected as RunningHub workflow")
    print(f"✓ Status: {result.status}")
    return True


async def example_mixed_usage():
    """Example 5: Mix local and cloud in same app"""
    print("\n=== Example 5: Mixed Local + Cloud ===")
    
    kit = ComfyKit()
    
    # Execute local workflow
    try:
        result_local = await kit.execute(
            "workflows/t2i_by_local_flux.json",
            {"prompt": "local"}
        )
        print(f"✓ Local execution: {result_local.status}")
    except:
        print("⚠️  Local ComfyUI not available")
    
    # Execute cloud workflow
    if os.getenv("RUNNINGHUB_API_KEY"):
        result_cloud = await kit.execute(
            "12345",
            {"prompt": "cloud"}
        )
        print(f"✓ Cloud execution: {result_cloud.status}")
    else:
        print("⚠️  RunningHub API key not set")
    
    print("✓ Same instance for both!")


async def main():
    print("☁️  ComfyKit RunningHub Cloud Examples")
    print("="*60)
    print("\n💡 RunningHub provides cloud GPU for ComfyUI workflows")
    print("   No local setup needed!\n")
    
    # Check configuration
    if not os.getenv("RUNNINGHUB_API_KEY"):
        print("⚠️  RUNNINGHUB_API_KEY environment variable not set")
        print("\nTo use RunningHub:")
        print("  1. Sign up at https://www.runninghub.ai")
        print("  2. Get your API key")
        print("  3. Set environment variable:")
        print("     export RUNNINGHUB_API_KEY='your-key-here'")
        print("\n" + "="*60)
        return
    
    try:
        success_count = 0
        success_count += await example_basic_cloud() or 0
        success_count += await example_with_config() or 0
        success_count += await example_same_params_format() or 0
        success_count += await example_auto_detection() or 0
        await example_mixed_usage()
        
        print("\n" + "="*60)
        print(f"✨ Completed {success_count} cloud examples!")
        print("\nNext: Check out 05_advanced_features.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Check:")
        print("   1. API key is valid")
        print("   2. Workflow ID exists")
        print("   3. Network connection")


if __name__ == "__main__":
    asyncio.run(main())

