from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

class SearchResult(BaseModel):
    chunks: List[str]
    distances: List[float]

class AskRequest(BaseModel):
    query: str
    top_k: int = 3
    model: str
    api_key: str

class AskResponse(BaseModel):
    answer: str
    chunks: List[str]

class PDFUploadResponse(BaseModel):
    success: bool
    message: str
    chunks_count: int
    filename: str

class ModelsResponse(BaseModel):
    models: List[str]