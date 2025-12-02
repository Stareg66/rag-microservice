import re

class Preprocess:

    def __init__(self):
        pass

    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = text.replace("\u00A0", " ")
        return text.strip()
    
    def chunk_text(self, text: str, chunk_size=500, overlap=80):
        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = start + chunk_size
            chunk = words[start:end]
            chunks.append(" ".join(chunk))
            start += chunk_size - overlap

        return chunks