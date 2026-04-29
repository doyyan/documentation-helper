import asyncio
import time
from typing import List
import aiohttp
import requests

# ==== SYNCHRONOUS VERSION (SLOW) ====
def sync_fetch_multiple_urls(urls: List[str]) -> List[str]:
    """Fetch multiple URLs synchronously - one at a time"""
    print("🐢 Synchronous fetching...")
    start_time = time.time()

    contents = []
    for i, url in enumerate(urls, 1):
        print(f"  Fetching {i}/{len(urls)}: {url}")
        try:
            response = requests.get(url, timeout=10)
            contents.append(response.text[:100] + "...")  # First 100 chars
        except Exception as e:
            contents.append(f"Error: {e}")

    end_time = time.time()
    print(f"  ⏱️  Sync completed in {end_time - start_time:.2f} seconds\n")
    return contents


# ==== ASYNCHRONOUS VERSION (FAST) ====
async def async_fetch_url(session: aiohttp.ClientSession, url: str, index: int, total: int) -> str:
    """Fetch a single URL asynchronously"""
    print(f"  🚀 Starting fetch {index}/{total}: {url}")
    try:
        async with session.get(url, timeout=10) as response:
            content = await response.text()
            print(f"  ✅ Completed fetch {index}/{total}")
            return content[:100] + "..."  # First 100 chars
    except Exception as e:
        print(f"  ❌ Failed fetch {index}/{total}: {e}")
        return f"Error: {e}"


async def async_fetch_multiple_urls(urls: List[str]) -> List[str]:
    """Fetch multiple URLs asynchronously - all at once"""
    print("🚀 Asynchronous fetching...")
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        # Create all tasks at once
        tasks = [
            async_fetch_url(session, url, i+1, len(urls))
            for i, url in enumerate(urls)
        ]

        # Run all tasks concurrently
        contents = await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"  ⏱️  Async completed in {end_time - start_time:.2f} seconds\n")
    return contents


# ==== DEMONSTRATION ====
async def demonstrate_async_speed():
    """Show the speed difference between sync and async"""
    print("=" * 60)
    print("🔍 ASYNC vs SYNC COMPARISON")
    print("=" * 60)

    # Test URLs (use httpbin.org for reliable testing)
    urls = [
        "https://httpbin.org/delay/1",  # 1 second delay
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1"
    ]

    print(f"📡 Fetching {len(urls)} URLs (each has 1s delay)")
    print()

    # Synchronous version
    sync_results = sync_fetch_multiple_urls(urls)

    # Asynchronous version
    async_results = await async_fetch_multiple_urls(urls)

    print("🎯 RESULTS:")
    print("  Sync: ~5+ seconds (1+1+1+1+1)")
    print("  Async: ~1+ seconds (all at once!)")
    print("  🏆 Async wins!")


# ==== YOUR DOCUMENTATION PIPELINE EXAMPLE ====
async def async_documentation_ingestion():
    """Example of async documentation ingestion"""
    print("\n" + "=" * 60)
    print("📚 ASYNC DOCUMENTATION INGESTION EXAMPLE")
    print("=" * 60)

    # Simulated documentation URLs
    doc_urls = [
        "https://docs.python.org/3/tutorial/introduction.html",
        "https://docs.python.org/3/tutorial/controlflow.html",
        "https://docs.python.org/3/tutorial/datastructures.html",
        "https://docs.python.org/3/library/os.html"
    ]

    async def process_doc_page(url: str) -> dict:
        """Process a single documentation page"""
        print(f"  🔄 Processing: {url.split('/')[-1]}")

        # Simulate: fetch content, extract text, create embeddings
        await asyncio.sleep(0.5)  # Simulate processing time

        return {
            "url": url,
            "content": f"Processed content from {url.split('/')[-1]}",
            "chunks": 5,  # Simulated chunk count
            "embeddings_created": True
        }

    print("🚀 Processing documentation pages concurrently...")

    # Process all pages at once
    tasks = [process_doc_page(url) for url in doc_urls]
    results = await asyncio.gather(*tasks)

    print("\n📊 Results:")
    for result in results:
        print(f"  ✅ {result['url'].split('/')[-1]}: {result['chunks']} chunks embedded")


# ==== ASYNC PATTERNS YOU'LL USE ====
async def common_async_patterns():
    """Common async patterns for your projects"""
    print("\n" + "=" * 60)
    print("🛠️  COMMON ASYNC PATTERNS")
    print("=" * 60)

    # Pattern 1: asyncio.gather() - Run multiple tasks concurrently
    print("1️⃣  asyncio.gather() - Run tasks concurrently:")

    async def task(name: str, delay: float):
        await asyncio.sleep(delay)
        return f"Task {name} completed"

    results = await asyncio.gather(
        task("A", 0.1),
        task("B", 0.1),
        task("C", 0.1)
    )
    print(f"   Results: {results}")

    # Pattern 2: asyncio.create_task() - Start task in background
    print("\n2️⃣  asyncio.create_task() - Background tasks:")

    task_a = asyncio.create_task(task("Background", 0.1))
    print("   Task started in background...")

    # Do other work
    await asyncio.sleep(0.05)
    print("   Did some other work...")

    # Wait for background task
    result = await task_a
    print(f"   Background result: {result}")

    # Pattern 3: async context manager
    print("\n3️⃣  Async context managers:")

    class AsyncResource:
        async def __aenter__(self):
            print("   📂 Opening async resource...")
            await asyncio.sleep(0.01)
            return self

        async def __aexit__(self, *args):
            print("   📫 Closing async resource...")
            await asyncio.sleep(0.01)

    async with AsyncResource() as resource:
        print("   💼 Using async resource...")
        await asyncio.sleep(0.01)


# ==== MAIN DEMO FUNCTION ====
async def main():
    """Run all async demonstrations"""
    try:
        await demonstrate_async_speed()
        await async_documentation_ingestion()
        await common_async_patterns()

        print("\n" + "=" * 60)
        print("🎉 ASYNC LEARNING COMPLETE!")
        print("=" * 60)
        print("Key takeaways:")
        print("  • Async is perfect for I/O operations (web requests, file reads)")
        print("  • Use 'await' to wait for results")
        print("  • Use 'asyncio.gather()' to run multiple tasks concurrently")
        print("  • 'asyncio.run()' is your entry point from sync world")

    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("💡 Note: Some demos need internet connection")


if __name__ == "__main__":
    # This is the standard way to run async code from a script
    asyncio.run(main())