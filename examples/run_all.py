"""
Run All Examples - Execute all ComfyKit examples

This script runs all examples to verify functionality and serve as integration tests.
"""

import asyncio
import sys
import time
from pathlib import Path

# Add parent directory to path so we can import comfykit
sys.path.insert(0, str(Path(__file__).parent.parent))


# Get all example files
EXAMPLES_DIR = Path(__file__).parent
EXAMPLE_FILES = sorted([
    f for f in EXAMPLES_DIR.glob("*.py")
    if f.name.startswith(("01_", "02_", "03_", "04_", "05_"))
])


async def run_example(example_file: Path) -> tuple[str, bool, float, str]:
    """Run a single example and return results
    
    Returns:
        (name, success, duration, error_msg)
    """
    name = example_file.stem
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print('='*60)
    
    start_time = time.time()
    
    try:
        # Import and run the example's main()
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, example_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'main'):
            await module.main()
        
        duration = time.time() - start_time
        return (name, True, duration, "")
        
    except Exception as e:
        duration = time.time() - start_time
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"\n❌ Error in {name}: {error_msg}")
        return (name, False, duration, error_msg)


async def main():
    """Run all examples and report results"""
    print("🚀 Running All ComfyKit Examples")
    print("="*60)
    print(f"\nFound {len(EXAMPLE_FILES)} examples:")
    for f in EXAMPLE_FILES:
        print(f"  - {f.stem}")
    print()
    
    # Run all examples
    results = []
    for example_file in EXAMPLE_FILES:
        result = await run_example(example_file)
        results.append(result)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    success_count = sum(1 for _, success, _, _ in results if success)
    total_count = len(results)
    total_duration = sum(duration for _, _, duration, _ in results)
    
    for name, success, duration, error in results:
        status = "✅" if success else "❌"
        print(f"{status} {name:<30} {duration:.2f}s")
        if not success:
            print(f"   Error: {error}")
    
    print("\n" + "-"*60)
    print(f"Passed: {success_count}/{total_count}")
    print(f"Failed: {total_count - success_count}/{total_count}")
    print(f"Total time: {total_duration:.2f}s")
    print("="*60)
    
    # Exit with appropriate code
    if success_count == total_count:
        print("\n✨ All examples passed!")
        return 0
    else:
        print(f"\n⚠️  {total_count - success_count} example(s) failed")
        print("\n💡 Some failures are expected if:")
        print("   - ComfyUI is not running locally")
        print("   - RUNNINGHUB_API_KEY is not set")
        print("   - Required workflows are missing")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

