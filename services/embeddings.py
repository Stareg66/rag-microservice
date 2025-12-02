from fastembed.embedding import TextEmbedding

class EmbeddingService:

    def __init__(self):
        self.embedder = None

    def load_model(self):
        if self.embedder is None:
            print("Loading model..")
            self.embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
            print("Model loaded")

    def generate_embeddings(self, texts: list[str]):
        if self.embedder is None:
            raise RuntimeError("Model is not loaded.")
        
        vectors = list(self.embedder.embed(texts))
        return [v.tolist() for v in vectors]