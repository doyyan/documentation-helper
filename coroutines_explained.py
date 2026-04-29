import asyncio
import time

# ==== UNDERSTANDING COROUTINES vs FUNCTION CALLS ====

def regular_function(name):
    """A regular synchronous function"""
    print(f"🔵 Regular function executing: {name}")
    time.sleep(0.1)  # Simulate work
    return f"Result from {name}"

async def async_function(name):
    """An async function that returns a coroutine"""
    print(f"🟢 Async function executing: {name}")
    await asyncio.sleep(0.1)  # Simulate async work
    return f"Async result from {name}"

def demonstrate_function_types():
    """Show the difference between functions, function calls, and coroutines"""

    print("=" * 80)
    print("🔍 FUNCTIONS vs FUNCTION CALLS vs COROUTINES")
    print("=" * 80)

    # 1. Function REFERENCE (higher-order function concept you know)
    print("1️⃣ Function Reference (what you already know):")
    func_ref = regular_function  # No parentheses - just the function object
    print(f"   func_ref = {func_ref}")
    print(f"   Type: {type(func_ref)}")
    print("   💡 This is a reference to the function, not a call")

    # 2. Function CALL (immediate execution)
    print("\n2️⃣ Function Call (immediate execution):")
    result = regular_function("test")  # Parentheses - executes immediately!
    print(f"   result = {result}")
    print(f"   Type: {type(result)}")
    print("   💡 Function executed immediately, returned the result")

    # 3. COROUTINE (the magic you're asking about!)
    print("\n3️⃣ Coroutine (the thing you're asking about!):")
    coro = async_function("test")  # Parentheses but NO execution!
    print(f"   coro = {coro}")
    print(f"   Type: {type(coro)}")
    print("   💡 Function NOT executed! Returns a 'coroutine object'")
    print("   💡 This is a 'suspended function call' - ready to run later")

    # Clean up the coroutine to avoid warnings
    coro.close()

def demonstrate_list_of_coroutines():
    """Show what happens when you create a list of coroutines"""

    print("\n" + "=" * 80)
    print("📝 CREATING LISTS OF COROUTINES")
    print("=" * 80)

    urls = ["url1", "url2", "url3"]

    # Regular function calls (immediate execution)
    print("🔴 Regular functions - execute immediately:")
    regular_results = []
    for url in urls:
        result = regular_function(url)  # Executes right now!
        regular_results.append(result)
    print(f"   Results: {regular_results}")
    print("   💡 All functions executed during the loop")

    # Async function calls (create coroutines, NO execution)
    print("\n🟢 Async functions - create coroutines (no execution):")
    coroutines = []
    for url in urls:
        coro = async_function(url)  # Creates coroutine, does NOT execute!
        coroutines.append(coro)
    print(f"   Coroutines: {coroutines}")
    print("   💡 No functions executed yet! Just created coroutine objects")

    # List comprehension version (what you saw)
    print("\n✨ List comprehension version:")
    coro_list = [async_function(url) for url in urls]
    print(f"   [async_function(url) for url in urls] = {coro_list}")
    print("   💡 Same thing - list of coroutine objects, no execution")

    # Clean up coroutines
    for coro in coroutines + coro_list:
        coro.close()

async def demonstrate_coroutine_execution():
    """Show how coroutines actually get executed"""

    print("\n" + "=" * 80)
    print("⚡ HOW COROUTINES GET EXECUTED")
    print("=" * 80)

    urls = ["page1", "page2", "page3"]

    # Step 1: Create coroutines (no execution)
    print("📍 Step 1: Creating coroutines...")
    coroutines = [async_function(url) for url in urls]
    print(f"   Created: {len(coroutines)} coroutine objects")
    print("   💡 No functions have executed yet!")

    # Step 2: Execute with asyncio.gather
    print("\n📍 Step 2: Executing with asyncio.gather...")
    print("   await asyncio.gather(*coroutines)")
    print("   💡 NOW the functions will execute!")

    results = await asyncio.gather(*coroutines)
    print(f"   Results: {results}")

def demonstrate_the_magic():
    """Show the magic step-by-step"""

    print("\n" + "=" * 80)
    print("🎩 THE MAGIC REVEALED")
    print("=" * 80)

    urls = ["doc1", "doc2", "doc3"]

    print("🔍 What you thought was happening:")
    print("   scrape_page(url1), scrape_page(url2), scrape_page(url3)")
    print("   ↑ You thought these were function CALLS")

    print("\n✨ What's actually happening:")
    print("   scrape_page(url1) → coroutine object 1 (not executed)")
    print("   scrape_page(url2) → coroutine object 2 (not executed)")
    print("   scrape_page(url3) → coroutine object 3 (not executed)")
    print("   ↑ These are coroutine OBJECTS, not results!")

    print("\n📊 Visual representation:")

    async def mock_scrape_page(url):
        """Mock scraping function for demonstration"""
        await asyncio.sleep(0.01)
        return f"Content from {url}"

    # Create the coroutines
    coro1 = mock_scrape_page("doc1")
    coro2 = mock_scrape_page("doc2")
    coro3 = mock_scrape_page("doc3")

    print(f"   coro1 = {coro1}")
    print(f"   coro2 = {coro2}")
    print(f"   coro3 = {coro3}")
    print("\n   💡 See? They're coroutine objects, not strings!")

    # Clean up
    coro1.close()
    coro2.close()
    coro3.close()

async def demonstrate_timing():
    """Show when execution actually happens"""

    print("\n" + "=" * 80)
    print("⏰ TIMING: WHEN EXECUTION HAPPENS")
    print("=" * 80)

    async def timed_function(name):
        print(f"      ⚡ {name} ACTUALLY executing at {time.time():.2f}")
        await asyncio.sleep(0.1)
        print(f"      ✅ {name} finished at {time.time():.2f}")
        return f"Result from {name}"

    print("📍 Creating coroutines...")
    start_time = time.time()
    print(f"   Start time: {start_time:.2f}")

    # These create coroutines but don't execute
    coro1 = timed_function("Task-1")
    coro2 = timed_function("Task-2")
    coro3 = timed_function("Task-3")

    print(f"   Coroutines created at: {time.time():.2f}")
    print("   💡 No output from functions yet!")

    print("\n📍 Now executing with await...")
    results = await asyncio.gather(coro1, coro2, coro3)

    print(f"   All finished at: {time.time():.2f}")
    print(f"   Results: {results}")

async def practical_documentation_example():
    """Show how this works in your documentation pipeline"""

    print("\n" + "=" * 80)
    print("📚 YOUR DOCUMENTATION PIPELINE EXAMPLE")
    print("=" * 80)

    async def tavily_extract_mock(url):
        """Mock Tavily extraction"""
        print(f"      🔄 Actually extracting from {url}")
        await asyncio.sleep(0.1)
        print(f"      ✅ Finished extracting from {url}")
        return f"Content from {url}"

    urls = [
        "https://langchain.com/docs/intro",
        "https://langchain.com/docs/modules",
        "https://langchain.com/docs/guides"
    ]

    print("🚀 Your code breakdown:")
    print("   contents = await asyncio.gather(*[tavily_extract.run(url) for url in urls])")

    print("\n📍 Step 1: List comprehension creates coroutines")
    coroutines = [tavily_extract_mock(url) for url in urls]
    print(f"   [tavily_extract_mock(url) for url in urls] = {coroutines}")
    print("   💡 No extraction happened yet!")

    print("\n📍 Step 2: * unpacks the coroutine list")
    print(f"   *{coroutines}")
    print("   becomes:")
    print(f"   asyncio.gather(coro1, coro2, coro3)")

    print("\n📍 Step 3: await executes all coroutines concurrently")
    contents = await asyncio.gather(*coroutines)
    print(f"   Results: {contents}")

def compare_with_regular_functions():
    """Compare with regular functions to make it crystal clear"""

    print("\n" + "=" * 80)
    print("⚖️  COMPARISON: REGULAR vs ASYNC FUNCTIONS")
    print("=" * 80)

    def regular_scrape(url):
        print(f"      🔵 Regular: Actually scraping {url} NOW")
        time.sleep(0.1)
        return f"Regular content from {url}"

    async def async_scrape(url):
        print(f"      🟢 Async: Actually scraping {url} NOW")
        await asyncio.sleep(0.1)
        return f"Async content from {url}"

    urls = ["site1", "site2"]

    print("🔴 Regular functions:")
    print("   results = [regular_scrape(url) for url in urls]")
    regular_results = [regular_scrape(url) for url in urls]  # Executes immediately!
    print(f"   💡 Functions executed during list creation!")
    print(f"   Results: {regular_results}")

    print("\n🟢 Async functions:")
    print("   coroutines = [async_scrape(url) for url in urls]")
    async_coroutines = [async_scrape(url) for url in urls]  # Creates coroutines only!
    print(f"   💡 No functions executed! Just created coroutines!")
    print(f"   Coroutines: {async_coroutines}")

    # Clean up
    for coro in async_coroutines:
        coro.close()

async def main():
    """Run all demonstrations"""

    print("🎓 COROUTINES: THE MYSTERY SOLVED!")
    print("Understanding suspended function calls")

    # Basic concepts
    demonstrate_function_types()
    demonstrate_list_of_coroutines()

    # Async demonstrations
    await demonstrate_coroutine_execution()
    demonstrate_the_magic()
    await demonstrate_timing()
    await practical_documentation_example()

    # Comparison
    compare_with_regular_functions()

    print("\n" + "=" * 80)
    print("🎯 THE BIG REVELATION")
    print("=" * 80)
    print("• async_function() creates a COROUTINE, not a result")
    print("• Coroutines are 'suspended function calls'")
    print("• They don't execute until you await them")
    print("• This is why async enables concurrency!")
    print("• Your list comprehension creates coroutines, not results")
    print("• asyncio.gather() is what actually executes them! 🚀")

if __name__ == "__main__":
    asyncio.run(main())