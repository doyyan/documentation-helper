import asyncio
import time
import threading

# Global counter to show event loop iterations
loop_iteration = 0

async def traced_operation(name: str, delay: float):
    """An operation that shows exactly when it runs"""
    print(f"  🟢 [{name}] STARTED at {time.time():.2f} (thread: {threading.current_thread().name})")

    # This is where the "yielding" happens
    print(f"  ⏸️  [{name}] About to YIELD to event loop (await asyncio.sleep)")
    await asyncio.sleep(delay)  # YIELDS control back to event loop

    print(f"  ✅ [{name}] RESUMED and FINISHED at {time.time():.2f}")
    return f"Result from {name}"

async def demonstrate_await_mechanics():
    """Show exactly what happens during await"""

    print("=" * 80)
    print("🔍 WHAT HAPPENS DURING 'await task'")
    print("=" * 80)

    print("📍 STEP 1: Creating tasks (scheduling in event loop)")
    # create_task() immediately schedules the task in the event loop
    task_a = asyncio.create_task(traced_operation("Task-A", 1.0))
    task_b = asyncio.create_task(traced_operation("Task-B", 0.5))

    print(f"   Tasks created at {time.time():.2f}")
    print(f"   Task-A status: {task_a.done()}")
    print(f"   Task-B status: {task_b.done()}")
    print("   💡 Tasks are now SCHEDULED but may not have started yet")

    print("\n📍 STEP 2: First await - what really happens")
    print("   About to: await task_a")
    print("   This will:")
    print("     1. Check if task_a is done (it's probably still running)")
    print("     2. If not done: YIELD control to event loop")
    print("     3. Event loop runs other tasks while we wait")
    print("     4. When task_a completes: event loop RESCHEDULES us")
    print("     5. We RESUME right here with the result")

    start_wait = time.time()
    result_a = await task_a  # THE MAGIC HAPPENS HERE
    end_wait = time.time()

    print(f"   ✅ Resumed with result: {result_a}")
    print(f"   ⏱️  We were 'yielded' for {end_wait - start_wait:.2f} seconds")

    print("\n📍 STEP 3: Second await - probably already done")
    print("   About to: await task_b")
    print(f"   Task-B status: {task_b.done()}")

    if task_b.done():
        print("   💨 Task already finished! await returns immediately")
    else:
        print("   ⏳ Task still running, will yield again...")

    result_b = await task_b
    print(f"   ✅ Got result: {result_b}")

async def show_event_loop_scheduling():
    """Show how the event loop schedules and manages tasks"""

    print("\n" + "=" * 80)
    print("⚙️  EVENT LOOP SCHEDULING VISUALIZATION")
    print("=" * 80)

    async def quick_task(name: str, duration: float):
        print(f"    🏃 {name} starts")
        await asyncio.sleep(duration)
        print(f"    🏁 {name} finishes")
        return name

    print("Creating 3 tasks that will interleave...")

    # These all get scheduled immediately
    task1 = asyncio.create_task(quick_task("Fast-Task", 0.1))
    task2 = asyncio.create_task(quick_task("Medium-Task", 0.2))
    task3 = asyncio.create_task(quick_task("Slow-Task", 0.3))

    print("\n📊 Now watching the event loop work...")
    print("   (Notice how tasks interleave - that's the event loop scheduling!)")

    # Await them in different order than creation
    print("\n🎯 Awaiting Slow-Task first (but others are running too):")
    result3 = await task3

    print(f"\n🎯 Awaiting Fast-Task (probably already done):")
    result1 = await task1

    print(f"\n🎯 Awaiting Medium-Task (probably already done):")
    result2 = await task2

    print(f"\n✅ Final results: {[result1, result2, result3]}")

async def demonstrate_yielding():
    """Show the 'yielding' concept in detail"""

    print("\n" + "=" * 80)
    print("🔄 UNDERSTANDING 'YIELDING' TO THE EVENT LOOP")
    print("=" * 80)

    async def yielding_function():
        print("    🟢 Function starts")
        print("    ⏸️  About to yield (await asyncio.sleep(0.1))")

        # This is the yield point - control goes back to event loop
        await asyncio.sleep(0.1)

        print("    ✅ Function resumes after yield")
        return "yielded result"

    async def background_work():
        """This will run while the other function is yielded"""
        for i in range(3):
            print(f"    🔧 Background work {i+1} happening during yield")
            await asyncio.sleep(0.03)  # Small delay

    print("Starting a function that will yield, plus background work...")

    # Start both concurrently
    main_task = asyncio.create_task(yielding_function())
    bg_task = asyncio.create_task(background_work())

    # Wait for both
    main_result = await main_task
    await bg_task

    print(f"✅ Main result: {main_result}")
    print("💡 Notice how background work happened DURING the main function's yield!")

async def await_vs_create_task_scheduling():
    """Compare what happens with await vs create_task at the event loop level"""

    print("\n" + "=" * 80)
    print("⚖️  AWAIT vs CREATE_TASK: EVENT LOOP PERSPECTIVE")
    print("=" * 80)

    async def test_operation(name: str):
        print(f"      🚀 {name} executing")
        await asyncio.sleep(0.1)
        print(f"      ✅ {name} complete")
        return name

    print("🔴 METHOD 1: Direct await (sequential scheduling)")
    start = time.time()

    print("  📍 await test_operation('First')")
    result1 = await test_operation("First")    # Schedules, yields, waits, resumes

    print("  📍 await test_operation('Second')")
    result2 = await test_operation("Second")   # Only starts after First completes

    print(f"  ⏱️  Sequential time: {time.time() - start:.2f}s")

    print("\n🔵 METHOD 2: create_task then await (concurrent scheduling)")
    start = time.time()

    print("  📍 create_task(test_operation('Third')) - SCHEDULES immediately")
    task3 = asyncio.create_task(test_operation("Third"))    # Schedules immediately

    print("  📍 create_task(test_operation('Fourth')) - SCHEDULES immediately")
    task4 = asyncio.create_task(test_operation("Fourth"))   # Also schedules immediately

    print("  📍 Both tasks are now running! Awaiting results...")
    result3 = await task3  # Just waits for completion
    result4 = await task4  # Just waits for completion

    print(f"  ⏱️  Concurrent time: {time.time() - start:.2f}s")

async def main():
    """Run all demonstrations"""

    print("🎓 EVENT LOOP & AWAIT DEEP DIVE")
    print("Understanding what really happens under the hood")

    await demonstrate_await_mechanics()
    await show_event_loop_scheduling()
    await demonstrate_yielding()
    await await_vs_create_task_scheduling()

    print("\n" + "=" * 80)
    print("🎯 KEY INSIGHTS")
    print("=" * 80)
    print("1. 'await task' does NOT schedule the task")
    print("   - create_task() schedules it")
    print("   - await just waits for completion")

    print("\n2. 'await' YIELDS control to event loop when waiting")
    print("   - If result ready: returns immediately")
    print("   - If not ready: yields, event loop runs other tasks")

    print("\n3. Event loop RESCHEDULES your coroutine when await completes")
    print("   - You resume right after the await statement")
    print("   - With the result value")

    print("\n4. This is why create_task() enables concurrency")
    print("   - Tasks scheduled immediately, all start running")
    print("   - await just waits for individual completion")

    print("\n🚀 Your documentation scraping benefits from this because:")
    print("   • All HTTP requests start immediately (create_task)")
    print("   • While waiting for responses, other requests continue")
    print("   • Event loop efficiently manages all I/O operations")

if __name__ == "__main__":
    asyncio.run(main())