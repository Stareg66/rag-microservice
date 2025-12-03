from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from services.pdf_loader import PDFLoader
from services.preprocess import Preprocess
from services.embeddings import EmbeddingService
from services.vector_store import Storage
from models import SearchRequest, SearchResult, PDFUploadResponse

# Create app
app = FastAPI(
    title="RAG Microservice API",
    description="Search in PDF API using RAG",
    version="1.0.0"
)

# Allow Tkinter connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize
loader = PDFLoader()
preprocess = Preprocess()
embedder = EmbeddingService()
storage = Storage()

# Create data/pdf folder
os.makedirs("./data/pdfs", exist_ok=True)

@app.on_event("startup")
async def startup_event():
    print("🚀 Initializing services...")
    storage.initialize_database()
    embedder.load_model()
    print("✅ Services ready!")

@app.get("/")
async def root():
    return {
        "message": "RAG Microservice API",
        "docs": "/docs",
        "status": "running"
    }

@app.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):

    # Validate PDF format
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    try:
        # Save PDF
        pdf_path = f"./data/pdfs/{file.filename}"
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process PDF
        text = loader.load_pdf(pdf_path)
        if not text:
            raise HTTPException(status_code=400, detail="Can't extract text from PDF")
        
        # Clean and chunk
        text = preprocess.clean_text(text)
        chunks = preprocess.chunk_text(text, chunk_size=500, overlap=80)
        
        # Generate embeddings
        embeddings = embedder.generate_embeddings(chunks)
        
        # Save in database
        storage.insert_chunks(chunks, embeddings)
        
        return PDFUploadResponse(
            success=True,
            message="PDF processed correctly",
            chunks_count=len(chunks),
            filename=file.filename
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
@app.post("/search", response_model=SearchResult)
async def search(request: SearchRequest):
    if storage.collection.count() == 0:
        raise HTTPException(status_code=400, detail="No indexed documents")
    
    try:
        # Generate query embedding
        query_emb = embedder.generate_embeddings([request.query])
        
        # Search in database
        results = storage.query(query_emb, top_k=request.top_k)
        
        return SearchResult(
            chunks=results["documents"][0],
            distances=results["distances"][0]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in search: {str(e)}")
    
@app.delete("/clear")
async def clear_database():
    try:
        storage.client.delete_collection(name="documents")
        storage.collection = storage.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        return {"success": True, "message": "Database clean"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cleaning DB: {str(e)}")
    
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)