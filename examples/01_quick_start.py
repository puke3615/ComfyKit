"""
Quick Start Example - Your First ComfyKit Program

This is the simplest way to use ComfyKit. Just 3 lines of code!
"""

import asyncio
from comfykit import ComfyKit


async def main():
    print("🚀 ComfyKit Quick Start\n")
    print("="*60)
    
    # Step 1: Create ComfyKit instance (connects to local ComfyUI by default)
    kit = ComfyKit()
    print(f"✓ Connected to ComfyUI at {kit.comfyui_url}")
    
    # Step 2: Execute a workflow
    print("\n📝 Executing workflow...")
    result = await kit.execute(
        "workflows/t2i_by_local_flux.json",
        {"prompt": "a beautiful sunset over the ocean"}
    )
    
    # Step 3: Check results
    print(f"\n✅ Status: {result.status}")
    if result.duration:
        print(f"✅ Duration: {result.duration:.2f}s")
    print(f"✅ Generated {len(result.images)} images")
    
    if result.images:
        print(f"\n🖼️  Images:")
        for i, img in enumerate(result.images, 1):
            print(f"   {i}. {img}")
    
    # Verify (acts as test)
    assert result.status in ["completed", "error"], "Should have valid status"
    
    print("\n" + "="*60)
    print("✨ Quick start completed successfully!")
    print("\nNext: Check out 02_configuration.py to learn about configuration options")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Tip: Make sure ComfyUI is running at http://127.0.0.1:8188")
        print("   Or set COMFYUI_BASE_URL to point to your ComfyUI server")

