import asyncio
import time

async def fetch_data(name: str, delay: float):
    """Simulate an async operation"""
    print(f"🚀 {name} started at {time.time():.2f}")
    await asyncio.sleep(delay)
    print(f"✅ {name} finished at {time.time():.2f}")
    if name == "Task-Error" and delay > 1:
        raise ValueError(f"Simulated error in {name}")
    return f"Result from {name}"

# ==== METHOD 1: asyncio.gather() ====
async def using_gather():
    """Using asyncio.gather - simple but less control"""
    print("🔵 METHOD 1: asyncio.gather()")
    start_time = time.time()
    print(f"   Start time: {start_time:.2f}")

    # gather() takes COROUTINES (not tasks) and handles everything
    results = await asyncio.gather(
        fetch_data("Task-A", 2.0),   # Coroutine (not started yet)
        fetch_data("Task-B", 1.0),   # Coroutine (not started yet)
        fetch_data("Task-C", 1.5),   # Coroutine (not started yet)
    )

    print(f"📊 Results: {results}")
    print(f"⏱️  Total time: {time.time() - start_time:.2f}s\n")

# ==== METHOD 2: create_task() + manual await ====
async def using_create_task():
    """Using create_task - more control, more verbose"""
    print("🟢 METHOD 2: asyncio.create_task()")
    start_time = time.time()
    print(f"   Start time: {start_time:.2f}")

    # create_task() creates and STARTS tasks immediately
    task_a = asyncio.create_task(fetch_data("Task-A", 2.0))  # Starts NOW
    task_b = asyncio.create_task(fetch_data("Task-B", 1.0))  # Starts NOW
    task_c = asyncio.create_task(fetch_data("Task-C", 1.5))  # Starts NOW

    print("💡 All tasks are already running...")

    # Now we await each task individually
    result_a = await task_a
    result_b = await task_b
    result_c = await task_c

    results = [result_a, result_b, result_c]
    print(f"📊 Results: {results}")
    print(f"⏱️  Total time: {time.time() - start_time:.2f}s\n")

# ==== METHOD 3: create_task() + gather() ====
async def using_create_task_with_gather():
    """Hybrid approach - create tasks explicitly, then gather"""
    print("🟡 METHOD 3: create_task() + gather()")
    start_time = time.time()
    print(f"   Start time: {start_time:.2f}")

    # Create tasks explicitly (gives you task objects)
    task_a = asyncio.create_task(fetch_data("Task-A", 2.0))
    task_b = asyncio.create_task(fetch_data("Task-B", 1.0))
    task_c = asyncio.create_task(fetch_data("Task-C", 1.5))

    print("💡 All tasks created and running...")

    # Use gather on the task objects
    results = await asyncio.gather(task_a, task_b, task_c)

    print(f"📊 Results: {results}")
    print(f"⏱️  Total time: {time.time() - start_time:.2f}s\n")

# ==== KEY DIFFERENCES DEMONSTRATION ====
async def demonstrate_key_differences():
    """Show the important differences between the approaches"""

    print("=" * 80)
    print("🔍 KEY DIFFERENCES DEMONSTRATION")
    print("=" * 80)

    # Difference 1: Task lifecycle control
    print("1️⃣  TASK LIFECYCLE CONTROL:")
    print("   gather(): Creates tasks internally, you can't access them")
    print("   create_task(): You get task objects, can check status, cancel, etc.")

    print("\n   Example - Getting task status:")

    # With create_task - you can check task status
    task = asyncio.create_task(fetch_data("Status-Check", 0.1))
    print(f"   Task created: {task}")
    print(f"   Task done? {task.done()}")

    await task  # Wait for it to finish
    print(f"   Task done now? {task.done()}")
    print(f"   Task result: {task.result()}")

    # Difference 2: Error handling
    print("\n2️⃣  ERROR HANDLING:")

    print("   gather(): If one fails, ALL fail (unless return_exceptions=True)")
    try:
        results = await asyncio.gather(
            fetch_data("Good-1", 0.1),
            fetch_data("Task-Error", 1.5),  # This will fail
            fetch_data("Good-2", 0.1),
            return_exceptions=False  # Default behavior
        )
    except ValueError as e:
        print(f"   ❌ gather() failed: {e}")

    print("   create_task(): You can handle each task's errors individually")
    task1 = asyncio.create_task(fetch_data("Good-1", 0.1))
    task2 = asyncio.create_task(fetch_data("Task-Error", 1.5))
    task3 = asyncio.create_task(fetch_data("Good-2", 0.1))

    # Handle each task individually
    try:
        result1 = await task1
        print(f"   ✅ Task1 success: {result1}")
    except Exception as e:
        print(f"   ❌ Task1 failed: {e}")

    try:
        result2 = await task2
        print(f"   ✅ Task2 success: {result2}")
    except Exception as e:
        print(f"   ❌ Task2 failed: {e}")

    try:
        result3 = await task3
        print(f"   ✅ Task3 success: {result3}")
    except Exception as e:
        print(f"   ❌ Task3 failed: {e}")

# ==== WHEN TO USE WHICH ====
async def when_to_use_which():
    """Guidelines on when to use gather vs create_task"""

    print("\n" + "=" * 80)
    print("🎯 WHEN TO USE WHICH?")
    print("=" * 80)

    print("🔵 USE asyncio.gather() WHEN:")
    print("   • You want simple, clean code")
    print("   • All tasks are equally important")
    print("   • You want results in the same order as input")
    print("   • You don't need to cancel or monitor individual tasks")
    print("   • Error handling can be done at the group level")

    print("\n🟢 USE create_task() WHEN:")
    print("   • You need to monitor individual task progress")
    print("   • You might need to cancel specific tasks")
    print("   • You want different error handling per task")
    print("   • You want to start tasks at different times")
    print("   • You need the task objects for other operations")

    print("\n🟡 HYBRID APPROACH (create_task + gather):")
    print("   • Best of both worlds")
    print("   • Explicit task creation + clean waiting")
    print("   • Good for complex scenarios")

# ==== YOUR DOCUMENTATION PIPELINE EXAMPLES ====
async def documentation_pipeline_examples():
    """Show real examples for your documentation scraping"""

    print("\n" + "=" * 80)
    print("📚 YOUR DOCUMENTATION PIPELINE EXAMPLES")
    print("=" * 80)

    urls = [
        "https://docs.python.org/page1.html",
        "https://docs.python.org/page2.html",
        "https://docs.python.org/page3.html",
        "https://docs.python.org/page4.html"
    ]

    async def scrape_page(url: str):
        """Simulate scraping a page"""
        await asyncio.sleep(0.2)  # Simulate network request
        return f"Content from {url.split('/')[-1]}"

    # Scenario 1: Simple batch processing - use gather()
    print("🔵 Scenario 1: Simple batch processing")
    print("   All pages equally important, just want the content")

    start = time.time()
    contents = await asyncio.gather(*[scrape_page(url) for url in urls])
    print(f"   ✅ Scraped {len(contents)} pages in {time.time()-start:.2f}s")

    # Scenario 2: Progress monitoring - use create_task()
    print("\n🟢 Scenario 2: Progress monitoring")
    print("   Want to show progress as pages complete")

    start = time.time()
    tasks = [asyncio.create_task(scrape_page(url)) for url in urls]

    # Monitor progress
    completed = 0
    while completed < len(tasks):
        for i, task in enumerate(tasks):
            if task.done() and not hasattr(task, '_reported'):
                completed += 1
                task._reported = True  # Mark as reported
                print(f"   📄 Progress: {completed}/{len(tasks)} pages completed")
        await asyncio.sleep(0.05)  # Check every 50ms

    # Get all results
    results = [await task for task in tasks]
    print(f"   ✅ All pages processed in {time.time()-start:.2f}s")

async def main():
    """Run all demonstrations"""

    print("=" * 80)
    print("🔍 GATHER vs CREATE_TASK: THE COMPLETE GUIDE")
    print("=" * 80)

    await using_gather()
    await using_create_task()
    await using_create_task_with_gather()
    await demonstrate_key_differences()
    await when_to_use_which()
    await documentation_pipeline_examples()

    print("\n" + "=" * 80)
    print("🎓 SUMMARY")
    print("=" * 80)
    print("gather() = Simple and clean, less control")
    print("create_task() = More control, more verbose")
    print("Hybrid = Best of both worlds")
    print("Your choice depends on your specific needs! 🚀")

if __name__ == "__main__":
    asyncio.run(main())