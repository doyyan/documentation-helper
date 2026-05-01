from typing import Any, Dict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import ToolMessage
from langchain.tools import tool
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import os

load_dotenv()  # Load environment variables from .env file

# Initialize embeddings (same as ingestion.py)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    show_progress_bar=True,  # Show progress for better UX
    chunk_size=1000,         # Increase for better throughput (max 2048 for text-embedding-3-large)
    retry_min_seconds=4,     # Reduce retry delay for faster recovery
    max_retries=3,           # Add explicit retry limit
)

vectorstore = PineconeVectorStore(
    index_name=os.getenv("INDEX_NAME", "medium-blogs-embeddings-index"),
    embedding=embeddings
)

# Initialize chat model
model = init_chat_model(os.getenv("DEFAULT_MODEL"), model_provider="openai")

@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve relevant documentation to help answer user queries about LangChain."""
    # Retrieve top 4 most similar documents
    retrieved_docs = vectorstore.as_retriever().invoke(query, k=4)

    # Serialize documents for the model
    serialized = "\n\n".join(
        (f"Source: {doc.metadata.get('source', 'Unknown')}\n\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )

    # Return both serialized content and raw documents
    return serialized, retrieved_docs

def run_llm(query: str) -> Dict[str, Any]:
    """
    Run the RAG pipeline to answer a query using retrieved documentation.

    Args:
        query: The user's question

    Returns:
        Dictionary containing:
            - answer: The generated answer
            - context: List of retrieved documents
    """
    # Create the agent with retrieval tool
    system_prompt = (
        "You are a helpful AI assistant that answers questions about LangChain documentation. "
        "You have access to a tool that retrieves relevant documentation. "
        "Use the tool to find relevant information before answering questions. "
        "Always cite the sources you use in your answers. "
        "If you cannot find the answer in the retrieved documentation, say so."
    )

    agent = create_agent(model, tools=[retrieve_context], system_prompt=system_prompt)
