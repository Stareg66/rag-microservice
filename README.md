# 📚 RAG Microservice - PDF Question Answering System

A production-ready **Retrieval-Augmented Generation (RAG)** microservice that enables intelligent semantic search and AI-powered question answering over PDF documents. Built with a clean client-server architecture using **FastAPI** for the backend and **Tkinter** for the desktop client.

![RAG Assistant Overview](https://gyazo.com/2c209ad1ea632770efd1ad8e052d0b45.png)

## 🎯 Features

- **📄 PDF Processing**: Upload and automatically process PDF documents with intelligent text extraction
- **🔍 Semantic Search**: Find relevant document sections using advanced embedding-based similarity search
- **🤖 AI-Powered Q&A**: Optional integration with OpenRouter for natural language answers (supports multiple LLM models)
- **💾 Persistent Storage**: ChromaDB vector database for efficient document storage and retrieval
- **🎨 Modern UI**: Clean, intuitive desktop interface built with Tkinter
- **🔌 REST API**: Well-documented FastAPI backend with automatic Swagger documentation
- **⚡ High Performance**: Asynchronous processing with FastEmbed for rapid embedding generation

---

## 🏗️ Architecture

This project implements a **microservice architecture** with clear separation between frontend and backend:

```
┌─────────────────┐         HTTP/REST API        ┌─────────────────┐
│                 │ ◄──────────────────────────► │                 │
│  Tkinter Client │         (localhost:8000)     │  FastAPI Server │
│   (Frontend)    │                              │    (Backend)    │
│                 │                              │                 │
└─────────────────┘                              └────────┬────────┘
                                                          │
                                                          │ Uses
                                                          ▼
                                         ┌────────────────────────────┐
                                         │       Service Layer        │
                                         ├────────────────────────────┤
                                         │ • PDF Loader               │
                                         │ • Text Preprocessor        │
                                         │ • Embedding Service        │
                                         │ • Vector Store (ChromaDB)  │
                                         │ • LLM Service (OpenRouter) │
                                         └────────────────────────────┘
```

### Backend Components

#### **FastAPI Server** (`backend/main.py`)
- RESTful API with automatic documentation (`/docs`)
- CORS middleware for cross-origin requests
- Asynchronous endpoints for non-blocking operations
- Comprehensive error handling and validation

#### **Service Layer** (`backend/services/`)
The backend uses a modular service architecture with `__init__.py` for clean imports:

1. **`pdf_loader.py`**: Extracts text from PDF files using PyPDF
2. **`preprocess.py`**: Cleans and chunks text with configurable overlap
3. **`embeddings.py`**: Generates vector embeddings using FastEmbed (BGE model)
4. **`vector_store.py`**: Manages ChromaDB for persistent vector storage
5. **`llm_service.py`**: Integrates with OpenRouter API for LLM responses

The `__init__.py` file exports all service functions, allowing clean imports like:
```python
from services import PDFLoader, EmbeddingService, Storage
```

#### **Data Models** (`backend/models.py`)
Pydantic models ensure type safety and automatic validation:
- `SearchRequest`: Query and result count parameters
- `SearchResult`: Retrieved chunks with similarity scores
- `AskRequest`: AI query with model selection
- `AskResponse`: Generated answer with source chunks
- `PDFUploadResponse`: Upload status and metadata

### Frontend

**Tkinter Desktop Client** (`frontend/app.py`)
- Modern, responsive UI with dark theme
- Real-time API health checks
- Threaded operations to prevent UI freezing
- Support for both semantic search and AI-powered Q&A modes

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/rag-microservice.git
cd rag-microservice
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start the backend server**
```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`
- View API documentation: `http://localhost:8000/docs`

4. **Launch the desktop client** (in a new terminal)
```bash
python frontend/app.py
```

---

## 📖 Usage

### Mode 1: Semantic Search (No API Key Required)

1. **Upload a PDF**: Click "📄 Load PDF" and select your document
2. **Wait for processing**: The system will extract, chunk, and embed the text
3. **Enter your query**: Type a search term in the query box
4. **View results**: See the most relevant document chunks with similarity scores

![Semantic Search Results](https://gyazo.com/4397435d46a40e028f677b7ac43508bd.png)

### Mode 2: AI-Powered Q&A (Requires OpenRouter API Key)

1. **Get an API key**: Sign up at [OpenRouter](https://openrouter.ai/) for free credits
2. **Enter your API key**: Paste it in the "OpenRouter API Key" field
3. **Load models**: Click "Load Models" to fetch available LLM options
4. **Select a model**: Choose from the dropdown (free and paid options available)
5. **Ask questions**: The system will now generate natural language answers using the PDF context

![AI-Powered Answer](https://gyazo.com/630192d0207bb2b43d81c43b166f88cb.png)

**Key Differences:**
- **Semantic Search**: Returns raw document chunks ranked by relevance
- **AI Mode**: Generates coherent, context-aware answers synthesizing information from multiple chunks

---

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API status and information |
| `GET` | `/docs` | Interactive API documentation |
| `GET` | `/health` | Health check endpoint |
| `POST` | `/upload-pdf` | Upload and process a PDF document |
| `POST` | `/search` | Semantic search in indexed documents |
| `POST` | `/ask` | AI-powered question answering |
| `POST` | `/models` | Fetch available OpenRouter models |
| `DELETE` | `/clear` | Clear the document database |

### Example API Usage

**Upload a PDF:**
```bash
curl -X POST "http://localhost:8000/upload-pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

**Search:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "top_k": 3}'
```

**Ask a Question (with AI):**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic?",
    "top_k": 3,
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "api_key": "your_openrouter_key"
  }'
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Framework** | FastAPI | High-performance async REST API |
| **Frontend** | Tkinter | Cross-platform desktop GUI |
| **PDF Processing** | PyPDF | Text extraction from PDFs |
| **Embeddings** | FastEmbed (BGE) | Fast, lightweight embedding generation |
| **Vector Database** | ChromaDB | Persistent similarity search |
| **LLM Integration** | OpenRouter API | Access to multiple AI models |
| **Data Validation** | Pydantic | Type-safe request/response models |

---

## 📁 Project Structure

```
rag-microservice/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py               # Pydantic data models
|   ├── data/pdfs               # Uploaded PDF storage
|   ├── chroma_db/                  # Vector database persistence
│   └── services/
│       ├── __init__.py         # Service exports for clean imports
│       ├── pdf_loader.py       # PDF text extraction
│       ├── preprocess.py       # Text cleaning and chunking
│       ├── embeddings.py       # Embedding generation (FastEmbed)
│       ├── vector_store.py     # ChromaDB integration
│       └── llm_service.py      # OpenRouter LLM client
├── frontend/
│   └── app.py                  # Tkinter desktop client                  
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 💡 Key Design Decisions

### 1. **Microservice Architecture**
- **Benefit**: Frontend and backend can be developed, tested, and scaled independently
- **Real-world use**: The API can serve multiple clients (web, mobile, CLI) simultaneously

### 2. **Service Layer with `__init__.py`**
- **Benefit**: Clean, organized imports and loose coupling between components
- **Example**: `from services import PDFLoader` instead of complex relative imports
- **Maintainability**: Easy to swap implementations (e.g., replace ChromaDB with Pinecone)

### 3. **FastAPI for Backend**
- **Benefit**: Automatic API documentation, async support, and Pydantic validation
- **Performance**: Non-blocking I/O for handling multiple requests efficiently
- **Developer Experience**: Interactive docs at `/docs` for testing and exploration

### 4. **ChromaDB for Vector Storage**
- **Benefit**: Persistent storage with built-in similarity search
- **Scalability**: Can handle large document collections with efficient indexing
- **Local-first**: No external database server required

### 5. **FastEmbed for Embeddings**
- **Benefit**: 10x faster than SentenceTransformers with similar accuracy
- **Resource-efficient**: Lightweight models suitable for local deployment
- **Quality**: Uses state-of-the-art BGE (BAAI General Embedding) models

### 6. **Optional LLM Integration**
- **Benefit**: System works out-of-the-box without API keys
- **Flexibility**: Users can choose between fast local search or AI-powered answers
- **Cost-effective**: Semantic search is free; AI mode uses pay-per-use pricing

---

## 🔒 Security Considerations

- API keys are **never stored** on disk or in logs
- CORS is configured for local development (restrict in production)
- File uploads are validated for PDF format
- Rate limiting should be added for production deployment

---

## 👨‍💻 Author

Built with ❤️ by Manuel Rueda Algar

Find me in Linkedin: [https://www.linkedin.com/in/manuelruedaalgar/](https://www.linkedin.com/in/manuelruedaalgar/)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [ChromaDB](https://www.trychroma.com/) for the vector database
- [FastEmbed](https://github.com/qdrant/fastembed) for efficient embeddings
- [OpenRouter](https://openrouter.ai/) for unified LLM API access
- The open-source community for inspiration and tools