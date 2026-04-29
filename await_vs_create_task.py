import asyncio
import time

async def fetch_data(name: str, delay: float):
    """Simulate fetching data with a delay"""
    print(f"🚀 Starting {name} (will take {delay}s)")
    await asyncio.sleep(delay)
    print(f"✅ Finished {name}")
    return f"Data from {name}"

# ==== METHOD 1: Direct await (SEQUENTIAL) ====
async def sequential_approach():
    """Using direct await - runs one after another"""
    print("🐢 SEQUENTIAL APPROACH (Direct await)")
    start = time.time()

    # These run ONE AT A TIME
    result1 = await fetch_data("API-1", 2.0)  # Wait 2 seconds
    result2 = await fetch_data("API-2", 1.5)  # Then wait 1.5 seconds
    result3 = await fetch_data("API-3", 1.0)  # Then wait 1 second

    end = time.time()
    print(f"⏱️  Sequential total time: {end - start:.2f} seconds")
    print(f"📊 Results: {[result1, result2, result3]}\n")

# ==== METHOD 2: create_task (CONCURRENT) ====
async def concurrent_approach():
    """Using create_task - runs all at the same time"""
    print("🚀 CONCURRENT APPROACH (create_task)")
    start = time.time()

    # These ALL START IMMEDIATELY
    task1 = asyncio.create_task(fetch_data("API-1", 2.0))  # Starts now
    task2 = asyncio.create_task(fetch_data("API-2", 1.5))  # Starts now
    task3 = asyncio.create_task(fetch_data("API-3", 1.0))  # Starts now

    print("💡 All tasks started! Now waiting for results...")

    # Now we wait for each result (they're running in parallel)
    result1 = await task1  # Wait for the longest one (2s)
    result2 = await task2  # Already finished!
    result3 = await task3  # Already finished!

    end = time.time()
    print(f"⏱️  Concurrent total time: {end - start:.2f} seconds")
    print(f"📊 Results: {[result1, result2, result3]}\n")

# ==== METHOD 3: asyncio.gather (EVEN CLEANER) ====
async def gather_approach():
    """Using asyncio.gather - cleanest concurrent approach"""
    print("✨ GATHER APPROACH (Most elegant)")
    start = time.time()

    # All start immediately and we wait for all to complete
    results = await asyncio.gather(
        fetch_data("API-1", 2.0),
        fetch_data("API-2", 1.5),
        fetch_data("API-3", 1.0)
    )

    end = time.time()
    print(f"⏱️  Gather total time: {end - start:.2f} seconds")
    print(f"📊 Results: {results}\n")

# ==== DEMONSTRATION FOR YOUR DOCUMENTATION PIPELINE ====
async def documentation_example():
    """Show how this applies to your documentation scraping"""
    print("=" * 60)
    print("📚 YOUR DOCUMENTATION PIPELINE EXAMPLE")
    print("=" * 60)

    urls = [
        "https://docs.python.org/page1",
        "https://docs.python.org/page2",
        "https://docs.python.org/page3",
        "https://docs.python.org/page4"
    ]

    async def scrape_page(url: str):
        """Simulate scraping a documentation page"""
        page_name = url.split('/')[-1]
        print(f"🔄 Scraping {page_name}...")
        await asyncio.sleep(1.0)  # Simulate network request
        print(f"✅ Scraped {page_name}")
        return f"Content from {page_name}"

    print("🚀 Scraping 4 documentation pages concurrently...")
    start = time.time()

    # Method 1: Sequential (SLOW)
    print("\n🐢 If you used sequential (direct await):")
    print("   await scrape_page(url1)  # 1 second")
    print("   await scrape_page(url2)  # 1 second")
    print("   await scrape_page(url3)  # 1 second")
    print("   await scrape_page(url4)  # 1 second")
    print("   Total: 4 seconds")

    # Method 2: Concurrent (FAST)
    print("\n🚀 Using create_task (concurrent):")
    tasks = [asyncio.create_task(scrape_page(url)) for url in urls]
    results = await asyncio.gather(*tasks)

    end = time.time()
    print(f"   ⏱️  Actual time: {end - start:.2f} seconds")
    print(f"   🎯 Speed improvement: ~4x faster!")

async def main():
    """Run all demonstrations"""
    print("=" * 60)
    print("🔍 AWAIT vs CREATE_TASK COMPARISON")
    print("=" * 60)

    await sequential_approach()
    await concurrent_approach()
    await gather_approach()
    await documentation_example()

    print("=" * 60)
    print("🎓 KEY TAKEAWAYS")
    print("=" * 60)
    print("• Direct await = Sequential (one after another)")
    print("• create_task() = Concurrent (all at once)")
    print("• asyncio.gather() = Cleanest concurrent pattern")
    print("• For I/O operations: concurrent = MUCH faster!")
    print("• Your doc scraping will be 3-10x faster with concurrency! 🚀")

if __name__ == "__main__":
    asyncio.run(main())