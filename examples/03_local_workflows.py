"""
Local Workflows Example - Execute ComfyUI Workflows Locally

Learn how to execute different types of workflows on your local ComfyUI server.
"""

import asyncio
from pathlib import Path
from comfykit import ComfyKit


async def example_basic_execution():
    """Example 1: Basic workflow execution"""
    print("\n=== Example 1: Basic Workflow ===")
    
    kit = ComfyKit()
    
    result = await kit.execute(
        "workflows/t2i_by_local_flux.json",
        {"prompt": "a cute cat playing with yarn"}
    )
    
    print(f"✓ Status: {result.status}")
    print(f"✓ Images: {len(result.images)}")
    
    # Verify
    assert result.status == "completed"
    assert result.prompt_id is not None


async def example_with_parameters():
    """Example 2: Workflow with custom parameters"""
    print("\n=== Example 2: Custom Parameters ===")
    
    kit = ComfyKit()
    
    result = await kit.execute(
        "workflows/t2i_by_local_flux.json",
        {
            "prompt": "a futuristic city at night",
            "seed": 42,
            "steps": 20
        }
    )
    
    print(f"✓ Status: {result.status}")
    print(f"✓ Duration: {result.duration:.2f}s")
    print(f"✓ Generated: {len(result.images)} images")
    
    # Verify
    assert result.status == "completed"
    assert result.duration > 0


async def example_from_dict():
    """Example 3: Execute from workflow dict"""
    print("\n=== Example 3: From Dictionary ===")
    
    kit = ComfyKit()
    
    # Load workflow as dict
    import json
    with open("workflows/t2i_by_local_flux.json") as f:
        workflow_dict = json.load(f)
    
    result = await kit.execute_json(
        workflow_dict,
        {"prompt": "a beautiful landscape"}
    )
    
    print(f"✓ Status: {result.status}")
    print(f"✓ Result type: dict → ExecuteResult")
    
    # Verify
    assert result.status == "completed"


async def example_from_url():
    """Example 4: Execute workflow from URL"""
    print("\n=== Example 4: From URL ===")
    
    kit = ComfyKit()
    
    # ComfyKit automatically downloads and executes
    result = await kit.execute(
        "https://example.com/workflow.json",  # URL workflow
        {"prompt": "a sunset"}
    )
    
    print(f"✓ URL workflow executed")
    print(f"✓ Status: {result.status}")


async def example_different_types():
    """Example 5: Different output types"""
    print("\n=== Example 5: Different Output Types ===")
    
    kit = ComfyKit()
    
    # Image output
    result = await kit.execute(
        "workflows/t2i_by_local_flux.json",
        {"prompt": "a robot"}
    )
    print(f"✓ Images: {len(result.images)}")
    
    # Video output (if you have video workflow)
    # result = await kit.execute(
    #     "workflows/t2v_by_local_wan_fusionx.json",
    #     {"prompt": "a flying bird"}
    # )
    # print(f"✓ Videos: {len(result.videos)}")
    
    # Text output (if you have text workflow)
    # result = await kit.execute(
    #     "workflows/i2t_by_local_florence.json",
    #     {"image": "path/to/image.png"}
    # )
    # print(f"✓ Texts: {len(result.texts)}")


async def example_result_handling():
    """Example 6: Handle execution results"""
    print("\n=== Example 6: Result Handling ===")
    
    kit = ComfyKit()
    
    result = await kit.execute(
        "workflows/t2i_by_local_flux.json",
        {"prompt": "a mountain"}
    )
    
    # Access results different ways
    print(f"✓ All images: {result.images}")
    print(f"✓ By variable: {result.images_by_var}")
    print(f"✓ Raw outputs: {result.outputs is not None}")
    
    # Check status
    if result.status == "completed":
        print("✓ Success!")
    else:
        print(f"✗ Failed: {result.msg}")
    
    # Verify
    assert result.status == "completed"
    assert isinstance(result.images, list)


async def main():
    print("🖼️  ComfyKit Local Workflows Examples")
    print("="*60)
    print("\n💡 These examples require a running local ComfyUI server")
    print("   Default: http://127.0.0.1:8188\n")
    
    try:
        await example_basic_execution()
        await example_with_parameters()
        await example_from_dict()
        # await example_from_url()  # Skip if no internet
        await example_different_types()
        await example_result_handling()
        
        print("\n" + "="*60)
        print("✨ All local workflow examples completed!")
        print("\nNext: Check out 04_runninghub_cloud.py for cloud execution")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure:")
        print("   1. ComfyUI is running")
        print("   2. Workflows exist in the workflows/ directory")
        print("   3. Required models are downloaded")


if __name__ == "__main__":
    asyncio.run(main())

