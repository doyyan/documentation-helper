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