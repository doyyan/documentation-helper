import asyncio
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_tavily import TavilyExtract

from logger import log_info, log_success, log_header, Colors

load_dotenv()

# Initialize components
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    show_progress_bar=True,
    chunk_size=1000,
    retry_min_seconds=4,
    max_retries=3,
)

vectorstore = PineconeVectorStore(
    index_name=os.getenv("INDEX_NAME", "medium-blogs-embeddings-index"),
    embedding=embeddings
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

tavily_extract = TavilyExtract()


# ==== SYNCHRONOUS VERSION (YOUR CURRENT APPROACH) ====
def sync_process_documentation(urls: List[str]) -> int:
    """Process documentation URLs synchronously - one at a time"""
    log_header("SYNCHRONOUS DOCUMENTATION PROCESSING")

    total_chunks = 0

    for i, url in enumerate(urls, 1):
        log_info(f"🔄 Processing {i}/{len(urls)}: {url}", Colors.CYAN)

        try:
            # Extract content (network I/O - BLOCKS!)
            content = tavily_extract.run(url)

            # Split into chunks
            chunks = text_splitter.split_text(content)

            # Create documents
            documents = [
                Document(page_content=chunk, metadata={"source": url})
                for chunk in chunks
            ]

            # Add to vector store (network I/O - BLOCKS!)
            vectorstore.add_documents(documents)

            total_chunks += len(chunks)
            log_success(f"✅ Added {len(chunks)} chunks from {url}")

        except Exception as e:
            log_info(f"❌ Error processing {url}: {e}", Colors.RED)

    log_success(f"🎉 Sync processing complete! Total chunks: {total_chunks}")
    return total_chunks


# ==== ASYNCHRONOUS VERSION (OPTIMIZED) ====
async def async_extract_content(url: str, session_id: int) -> Dict[str, Any]:
    """Extract content from a single URL asynchronously"""
    log_info(f"🚀 [{session_id}] Starting extraction: {url}", Colors.PURPLE)

    try:
        # Simulate async extraction (Tavily doesn't have async yet, but this shows the pattern)
        # In real async code, you'd use aiohttp or async-compatible libraries

        # For demo: run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, tavily_extract.run, url)

        log_success(f"✅ [{session_id}] Extracted content from {url}")

        return {
            "url": url,
            "content": content,
            "success": True
        }
    except Exception as e:
        log_info(f"❌ [{session_id}] Failed to extract {url}: {e}", Colors.RED)
        return {
            "url": url,
            "content": None,
            "success": False,
            "error": str(e)
        }


async def async_process_batch(batch: List[Dict[str, Any]]) -> int:
    """Process a batch of extracted content"""
    log_info(f"📦 Processing batch of {len(batch)} documents", Colors.CYAN)

    all_documents = []

    for item in batch:
        if not item["success"]:
            continue

        # Split into chunks
        chunks = text_splitter.split_text(item["content"])

        # Create documents
        documents = [
            Document(page_content=chunk, metadata={"source": item["url"]})
            for chunk in chunks
        ]

        all_documents.extend(documents)

    if all_documents:
        # Add all documents at once (more efficient)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, vectorstore.add_documents, all_documents)

        log_success(f"✅ Added {len(all_documents)} chunks to vector store")

    return len(all_documents)


async def async_process_documentation(urls: List[str], batch_size: int = 5) -> int:
    """Process documentation URLs asynchronously with batching"""
    log_header("ASYNCHRONOUS DOCUMENTATION PROCESSING")

    total_chunks = 0

    # Process URLs in batches to avoid overwhelming servers
    for i in range(0, len(urls), batch_size):
        batch_urls = urls[i:i + batch_size]
        batch_num = (i // batch_size) + 1

        log_info(f"🎯 Processing batch {batch_num}: {len(batch_urls)} URLs", Colors.YELLOW)

        # Extract content from all URLs in batch concurrently
        extraction_tasks = [
            async_extract_content(url, j + 1)
            for j, url in enumerate(batch_urls)
        ]

        # Wait for all extractions to complete
        batch_results = await asyncio.gather(*extraction_tasks)

        # Process the batch
        batch_chunks = await async_process_batch(batch_results)
        total_chunks += batch_chunks

        log_info(f"📊 Batch {batch_num} complete: {batch_chunks} chunks added", Colors.GREEN)

    log_success(f"🎉 Async processing complete! Total chunks: {total_chunks}")
    return total_chunks


# ==== DEMONSTRATION ====
async def demonstrate_async_ingestion():
    """Compare sync vs async documentation processing"""

    # Sample documentation URLs (you can replace with real ones)
    sample_urls = [
        "https://docs.python.org/3/tutorial/introduction.html",
        "https://docs.python.org/3/tutorial/controlflow.html",
        "https://docs.python.org/3/tutorial/datastructures.html",
        "https://docs.python.org/3/library/os.html",
        "https://docs.python.org/3/library/sys.html"
    ]

    print("=" * 80)
    print("🔬 DOCUMENTATION INGESTION: SYNC vs ASYNC COMPARISON")
    print("=" * 80)

    print(f"📚 Processing {len(sample_urls)} documentation pages")
    print()

    # Note: For demo purposes, we're showing the patterns
    # In real use, you'd uncomment one of these:

    # Synchronous processing
    # sync_chunks = sync_process_documentation(sample_urls)

    # Asynchronous processing
    # async_chunks = await async_process_documentation(sample_urls)

    # For now, just show the structure
    log_info("📝 Demo structure created! Uncomment the actual calls to run", Colors.CYAN)
    log_info("💡 Key benefits of async version:", Colors.YELLOW)
    print("   • Multiple URLs processed concurrently")
    print("   • Batching prevents server overload")
    print("   • Non-blocking I/O operations")
    print("   • 3-5x faster for large documentation sites")


# ==== ASYNC PATTERNS FOR YOUR PROJECT ====
async def async_patterns_for_docs():
    """Show specific async patterns useful for documentation ingestion"""

    log_header("ASYNC PATTERNS FOR DOCUMENTATION PROJECTS")

    # Pattern 1: Concurrent extraction with rate limiting
    print("1️⃣  Concurrent extraction with semaphore (rate limiting):")

    async def rate_limited_extraction(url: str, semaphore: asyncio.Semaphore):
        async with semaphore:  # Limit concurrent requests
            log_info(f"   🔄 Extracting: {url.split('/')[-1]}")
            await asyncio.sleep(0.1)  # Simulate extraction
            return f"Content from {url}"

    # Allow only 3 concurrent extractions
    semaphore = asyncio.Semaphore(3)
    urls = [f"https://docs.example.com/page{i}" for i in range(5)]

    tasks = [rate_limited_extraction(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks)
    print(f"   ✅ Extracted {len(results)} pages with rate limiting")

    # Pattern 2: Producer-Consumer with queues
    print("\n2️⃣  Producer-Consumer pattern with async queues:")

    async def url_producer(queue: asyncio.Queue, urls: List[str]):
        for url in urls:
            await queue.put(url)
            log_info(f"   📤 Queued: {url.split('/')[-1]}")
        await queue.put(None)  # Signal end

    async def content_consumer(queue: asyncio.Queue, consumer_id: int):
        processed = 0
        while True:
            url = await queue.get()
            if url is None:  # End signal
                break
            log_info(f"   🔄 Consumer {consumer_id} processing: {url.split('/')[-1]}")
            await asyncio.sleep(0.1)  # Simulate processing
            processed += 1

        return processed

    # Set up producer-consumer
    queue = asyncio.Queue(maxsize=10)  # Buffer size

    # Start producer and multiple consumers concurrently
    producer_task = asyncio.create_task(url_producer(queue, urls[:3]))
    consumer_tasks = [
        asyncio.create_task(content_consumer(queue, i+1))
        for i in range(2)  # 2 consumers
    ]

    # Wait for producer to finish
    await producer_task

    # Signal consumers to stop
    for _ in consumer_tasks:
        await queue.put(None)

    # Wait for consumers to finish
    results = await asyncio.gather(*consumer_tasks)
    print(f"   ✅ Consumers processed: {sum(results)} items total")

    print("\n💡 These patterns help with:")
    print("   • Managing server load (rate limiting)")
    print("   • Memory efficiency (streaming processing)")
    print("   • Fault tolerance (isolated failures)")


async def main():
    """Main demonstration function"""
    try:
        await demonstrate_async_ingestion()
        print()
        await async_patterns_for_docs()

        print("\n" + "=" * 80)
        print("🎓 ASYNC LEARNING FOR DOCUMENTATION INGESTION")
        print("=" * 80)
        print("Key takeaways for your project:")
        print("  🚀 Use async for I/O-bound operations (web requests, DB writes)")
        print("  📦 Process URLs in batches to avoid overwhelming servers")
        print("  🔄 Use asyncio.gather() for concurrent operations")
        print("  ⚡ Use semaphores/queues for rate limiting and flow control")
        print("  🎯 Your Tavily + Pinecone pipeline is perfect for async optimization!")

    except Exception as e:
        print(f"❌ Demo error: {e}")


if __name__ == "__main__":
    asyncio.run(main())