import chromadb
import os

class Storage:

    def __init__(self):
        self.client = None
        self.collection = None

    def initialize_database(self):
        if self.client is None:
            os.makedirs("./chroma_db", exist_ok=True)
            self.client = chromadb.PersistentClient(path="./chroma_db")
            self.collection = self.client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
            print("[Storage] ChromaDB connected")

    def insert_chunks(self, texts: list[str], embeddings: list[list[float]]):
        ids = [f"doc_{i}" for i in range(len(texts))]
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids
        )
        print(f"[Storage] Inserted {len(texts)} chunks")

    def query(self, query_embedding, top_k=3):
        return self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
