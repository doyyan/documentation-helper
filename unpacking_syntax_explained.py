import asyncio

# ==== THE * UNPACKING OPERATOR EXPLAINED ====

def demonstrate_unpacking_basics():
    """Show what the * operator does with regular functions"""

    print("=" * 60)
    print("🔍 UNDERSTANDING THE * UNPACKING OPERATOR")
    print("=" * 60)

    def add_three_numbers(a, b, c):
        """A function that takes 3 separate arguments"""
        return a + b + c

    # Method 1: Pass arguments individually
    result1 = add_three_numbers(1, 2, 3)
    print(f"add_three_numbers(1, 2, 3) = {result1}")

    # Method 2: Using unpacking with a list
    numbers = [1, 2, 3]
    result2 = add_three_numbers(*numbers)  # * unpacks the list
    print(f"add_three_numbers(*[1, 2, 3]) = {result2}")
    print(f"  💡 The * unpacked {numbers} into separate arguments")

    print(f"\n🔄 What * does:")
    print(f"  add_three_numbers(*[1, 2, 3])")
    print(f"  becomes:")
    print(f"  add_three_numbers(1, 2, 3)")

    # This would NOT work:
    try:
        # add_three_numbers([1, 2, 3])  # Would pass ONE list argument
        pass
    except TypeError as e:
        print(f"❌ Without *: {e}")

def demonstrate_list_comprehension_unpacking():
    """Show unpacking with list comprehensions"""

    print("\n" + "=" * 60)
    print("📝 LIST COMPREHENSION + UNPACKING")
    print("=" * 60)

    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]

    def fake_scrape_page(url):
        """Simulate scraping a page"""
        return f"Content from {url.split('/')[-1]}"

    # Step 1: List comprehension creates a list
    scraped_list = [fake_scrape_page(url) for url in urls]
    print(f"List comprehension result:")
    print(f"  {scraped_list}")

    # Step 2: Function that takes multiple arguments
    def combine_results(*results):
        """Function that takes any number of arguments"""
        return " | ".join(results)

    # Method 1: Pass the list as-is (WRONG)
    try:
        wrong_result = combine_results(scraped_list)
        print(f"\n❌ Passing list directly: {wrong_result}")
        print(f"  💡 This passes ONE argument (the whole list)")
    except:
        pass

    # Method 2: Unpack the list (CORRECT)
    right_result = combine_results(*scraped_list)
    print(f"\n✅ Unpacking with *: {right_result}")
    print(f"  💡 This passes THREE separate arguments")

    # The magic one-liner:
    one_liner = combine_results(*[fake_scrape_page(url) for url in urls])
    print(f"\n🚀 One-liner: combine_results(*[scrape_page(url) for url in urls])")
    print(f"  Result: {one_liner}")

async def demonstrate_async_unpacking():
    """Show how this applies to async functions like asyncio.gather()"""

    print("\n" + "=" * 60)
    print("⚡ ASYNC UNPACKING WITH asyncio.gather()")
    print("=" * 60)

    async def async_scrape_page(url):
        """Simulate async scraping"""
        await asyncio.sleep(0.1)  # Simulate network delay
        return f"Async content from {url.split('/')[-1]}"

    urls = [
        "https://docs.python.org/page1",
        "https://docs.python.org/page2",
        "https://docs.python.org/page3"
    ]

    # Method 1: Manual (verbose)
    print("🔴 Manual method (verbose):")
    task1 = async_scrape_page(urls[0])
    task2 = async_scrape_page(urls[1])
    task3 = async_scrape_page(urls[2])
    results1 = await asyncio.gather(task1, task2, task3)
    print(f"  Results: {results1}")

    # Method 2: List comprehension + unpacking (elegant)
    print("\n🟢 List comprehension + unpacking (elegant):")

    # This creates a list of coroutines:
    coroutines = [async_scrape_page(url) for url in urls]
    print(f"  List of coroutines: {coroutines}")

    # Then we unpack them into gather():
    results2 = await asyncio.gather(*coroutines)
    print(f"  Results: {results2}")

    # Method 3: The beautiful one-liner:
    print("\n✨ The elegant one-liner:")
    results3 = await asyncio.gather(*[async_scrape_page(url) for url in urls])
    print(f"  Results: {results3}")

    print(f"\n🎯 What happened:")
    print(f"  *[async_scrape_page(url) for url in urls]")
    print(f"  becomes:")
    print(f"  async_scrape_page(urls[0]), async_scrape_page(urls[1]), async_scrape_page(urls[2])")

def demonstrate_other_unpacking_uses():
    """Show other common uses of unpacking"""

    print("\n" + "=" * 60)
    print("🛠️ OTHER UNPACKING USE CASES")
    print("=" * 60)

    # 1. Function arguments
    def greet(first, last, title=""):
        return f"{title} {first} {last}".strip()

    person = ["John", "Doe"]
    print(f"1️⃣ Function arguments:")
    print(f"  greet(*{person}) = '{greet(*person)}'")

    # 2. List/tuple creation
    numbers1 = [1, 2, 3]
    numbers2 = [4, 5, 6]
    combined = [*numbers1, *numbers2]
    print(f"\n2️⃣ List combination:")
    print(f"  [*{numbers1}, *{numbers2}] = {combined}")

    # 3. Dictionary unpacking (**)
    person_info = {"name": "Alice", "age": 30}
    address_info = {"city": "NYC", "state": "NY"}
    full_info = {**person_info, **address_info}
    print(f"\n3️⃣ Dictionary unpacking:")
    print(f"  {{**person, **address}} = {full_info}")

    # 4. Variable assignment
    values = [10, 20, 30, 40]
    first, *middle, last = values
    print(f"\n4️⃣ Variable assignment:")
    print(f"  first, *middle, last = {values}")
    print(f"  first={first}, middle={middle}, last={last}")

async def practical_documentation_examples():
    """Show practical examples for your documentation pipeline"""

    print("\n" + "=" * 60)
    print("📚 PRACTICAL EXAMPLES FOR YOUR PROJECT")
    print("=" * 60)

    # Simulate your documentation URLs
    doc_urls = [
        "https://langchain.com/docs/intro",
        "https://langchain.com/docs/modules",
        "https://langchain.com/docs/use-cases",
        "https://langchain.com/docs/guides"
    ]

    async def tavily_extract_mock(url):
        """Mock Tavily extraction"""
        await asyncio.sleep(0.1)
        return f"Extracted content from {url.split('/')[-1]}"

    print("🚀 Your documentation pipeline patterns:")

    # Pattern 1: Gather all pages
    print("\n1️⃣ Extract all pages concurrently:")
    print("   contents = await asyncio.gather(*[tavily_extract.run(url) for url in urls])")

    contents = await asyncio.gather(*[tavily_extract_mock(url) for url in doc_urls])
    for content in contents:
        print(f"   ✅ {content}")

    # Pattern 2: Create tasks then gather
    print("\n2️⃣ Create tasks then gather:")
    print("   tasks = [asyncio.create_task(extract(url)) for url in urls]")
    print("   results = await asyncio.gather(*tasks)")

    tasks = [asyncio.create_task(tavily_extract_mock(url)) for url in doc_urls]
    results = await asyncio.gather(*tasks)
    print(f"   ✅ Processed {len(results)} pages")

    # Pattern 3: Batch processing
    print("\n3️⃣ Batch processing:")
    batch_size = 2
    all_results = []

    for i in range(0, len(doc_urls), batch_size):
        batch_urls = doc_urls[i:i + batch_size]
        print(f"   Processing batch: {[url.split('/')[-1] for url in batch_urls]}")

        batch_results = await asyncio.gather(*[tavily_extract_mock(url) for url in batch_urls])
        all_results.extend(batch_results)

    print(f"   ✅ Total results: {len(all_results)}")

async def main():
    """Run all demonstrations"""

    print("🎓 THE * UNPACKING OPERATOR: COMPLETE GUIDE")

    # Basic concepts
    demonstrate_unpacking_basics()
    demonstrate_list_comprehension_unpacking()

    # Async applications
    await demonstrate_async_unpacking()

    # Other uses
    demonstrate_other_unpacking_uses()

    # Practical examples
    await practical_documentation_examples()

    print("\n" + "=" * 60)
    print("🎯 SUMMARY")
    print("=" * 60)
    print("• * unpacks a list/tuple into separate arguments")
    print("• [func(x) for x in items] creates a list")
    print("• *[func(x) for x in items] unpacks that list")
    print("• Perfect for asyncio.gather() with dynamic URL lists")
    print("• Your one-liner: await asyncio.gather(*[scrape(url) for url in urls])! 🚀")

if __name__ == "__main__":
    asyncio.run(main())