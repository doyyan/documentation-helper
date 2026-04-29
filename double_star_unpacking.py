import asyncio

def demonstrate_double_star_unpacking():
    """Show the ** operator for dictionary unpacking"""

    print("=" * 60)
    print("🔍 THE ** DICTIONARY UNPACKING OPERATOR")
    print("=" * 60)

    def create_user(name, age, city, country="USA"):
        """Function that takes keyword arguments"""
        return f"{name}, {age} years old, from {city}, {country}"

    # Method 1: Pass arguments manually
    result1 = create_user(name="Alice", age=30, city="NYC")
    print(f"Manual: {result1}")

    # Method 2: Use ** to unpack dictionary
    user_info = {"name": "Bob", "age": 25, "city": "SF"}
    result2 = create_user(**user_info)  # ** unpacks dict to keyword args
    print(f"Unpacked: {result2}")

    print(f"\n🔄 What ** does:")
    print(f"  create_user(**{{'name': 'Bob', 'age': 25, 'city': 'SF'}})")
    print(f"  becomes:")
    print(f"  create_user(name='Bob', age=25, city='SF')")

def demonstrate_both_operators():
    """Show * and ** together"""

    print("\n" + "=" * 60)
    print("⚡ USING * AND ** TOGETHER")
    print("=" * 60)

    def complex_function(arg1, arg2, arg3, name="Unknown", debug=False):
        """Function with both positional and keyword arguments"""
        return f"Args: {[arg1, arg2, arg3]}, Name: {name}, Debug: {debug}"

    # Data
    positional_args = ["A", "B", "C"]
    keyword_args = {"name": "Alice", "debug": True}

    # Using both * and **
    result = complex_function(*positional_args, **keyword_args)
    print(f"Result: {result}")

    print(f"\n🎯 What happened:")
    print(f"  *{positional_args} → arg1='A', arg2='B', arg3='C'")
    print(f"  **{keyword_args} → name='Alice', debug=True")

async def async_examples_with_both():
    """Show async examples using both * and **"""

    print("\n" + "=" * 60)
    print("🚀 ASYNC EXAMPLES WITH * AND **")
    print("=" * 60)

    async def fetch_with_config(url, timeout=5, headers=None, method="GET"):
        """Simulate async fetch with configuration"""
        await asyncio.sleep(0.1)
        return f"Fetched {url} with {method}, timeout={timeout}s"

    urls = ["https://api.com/users", "https://api.com/posts"]

    # Configuration for all requests
    default_config = {
        "timeout": 10,
        "method": "GET",
        "headers": {"User-Agent": "MyBot"}
    }

    print("🔵 Using ** for shared configuration:")

    # Method 1: Manual (verbose)
    results1 = await asyncio.gather(
        fetch_with_config(urls[0], **default_config),
        fetch_with_config(urls[1], **default_config)
    )

    # Method 2: List comprehension with both * and **
    results2 = await asyncio.gather(
        *[fetch_with_config(url, **default_config) for url in urls]
    )

    print(f"Results: {results2}")

def practical_documentation_examples():
    """Practical examples for your documentation helper"""

    print("\n" + "=" * 60)
    print("📚 PRACTICAL EXAMPLES FOR YOUR PROJECT")
    print("=" * 60)

    # Example 1: Tavily configuration
    tavily_config = {
        "max_depth": 2,
        "extract_depth": "advanced",
        "include_images": False
    }

    urls = ["https://docs.langchain.com", "https://docs.openai.com"]

    print("1️⃣ Tavily extraction with shared config:")
    print("   # All URLs use the same configuration")
    print("   tavily_results = [")
    for url in urls:
        print(f"       tavily_crawl.invoke({{'url': '{url}', **tavily_config}}),")
    print("   ]")

    # Example 2: OpenAI embeddings configuration
    embedding_config = {
        "model": "text-embedding-3-small",
        "chunk_size": 1000,
        "show_progress_bar": True
    }

    print(f"\n2️⃣ OpenAI embeddings with config:")
    print(f"   embeddings = OpenAIEmbeddings(**{embedding_config})")

    # Example 3: Pinecone configuration
    pinecone_config = {
        "index_name": "docs-index",
        "namespace": "langchain-docs"
    }

    print(f"\n3️⃣ Pinecone vector store:")
    print(f"   vectorstore = PineconeVectorStore(embedding=embeddings, **{pinecone_config})")

def real_world_patterns():
    """Show real-world patterns you'll use"""

    print("\n" + "=" * 60)
    print("🌟 REAL-WORLD PATTERNS")
    print("=" * 60)

    print("1️⃣ Configuration management:")
    print("""
    # settings.py
    OPENAI_CONFIG = {
        "model": "text-embedding-3-small",
        "chunk_size": 1000,
        "retry_min_seconds": 4
    }

    PINECONE_CONFIG = {
        "index_name": "docs-index",
        "namespace": "production"
    }

    # main.py
    embeddings = OpenAIEmbeddings(**OPENAI_CONFIG)
    vectorstore = PineconeVectorStore(embedding=embeddings, **PINECONE_CONFIG)
    """)

    print("2️⃣ Dynamic function calls:")
    print("""
    # Different extraction methods based on URL
    extraction_configs = {
        "langchain.com": {"max_depth": 3, "extract_depth": "advanced"},
        "openai.com": {"max_depth": 2, "extract_depth": "basic"},
    }

    for url in urls:
        domain = url.split('/')[2]
        config = extraction_configs.get(domain, {})
        result = tavily_crawl.invoke({"url": url, **config})
    """)

    print("3️⃣ Batch processing with configs:")
    print("""
    # Process URLs in batches with different settings
    batch_configs = [
        {"urls": api_urls, "timeout": 30, "retries": 3},
        {"urls": doc_urls, "timeout": 60, "retries": 1},
    ]

    for config in batch_configs:
        urls = config.pop("urls")  # Remove urls from config
        results = await asyncio.gather(
            *[fetch_url(url, **config) for url in urls]
        )
    """)

def main():
    """Run all demonstrations"""

    print("🎓 THE * AND ** UNPACKING OPERATORS")

    demonstrate_double_star_unpacking()
    demonstrate_both_operators()

    print("\n⚡ Running async examples...")
    asyncio.run(async_examples_with_both())

    practical_documentation_examples()
    real_world_patterns()

    print("\n" + "=" * 60)
    print("🎯 QUICK REFERENCE")
    print("=" * 60)
    print("• *  unpacks lists/tuples → separate positional arguments")
    print("• ** unpacks dictionaries → separate keyword arguments")
    print("• Use together: function(*args, **kwargs)")
    print("• Perfect for configuration management! 🚀")

if __name__ == "__main__":
    main()