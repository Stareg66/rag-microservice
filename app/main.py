import chromadb
from chromadb.config import Settings
from fastembed.embedding import TextEmbedding

client = chromadb.Client(Settings(
    persist_directory="./storage",
    anonymized_telemetry=False
))

collection = client.get_or_create_collection(
    name="embedded_documents",
    metadata={"hnsw:space": "cosine"}
)

embedder = TextEmbedding(model_name="bge-small-en")