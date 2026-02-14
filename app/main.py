from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
import os
import shutil

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pre-initialize embeddings on startup
@app.on_event("startup")
async def startup_event():
    """Pre-warm the embedding model for faster first request"""
    try:
        from app.infrastructure.embeddings import generate_embedding
        print("🔥 Pre-warming embedding model...")
        _ = generate_embedding("initialization")
        print("✓ Embedding model ready")
    except Exception as e:
        print(f"⚠️ Embedding warm-up failed: {e}")

# Import routers
try:
    from app.api.routers.ingestion import router as ingestion_router
    app.include_router(ingestion_router)
except Exception as e:
    print(f"Warning: Could not load ingestion router: {e}")

try:
    from app.api.routers.policy import router as policy_router
    app.include_router(policy_router)
except Exception as e:
    print(f"Warning: Could not load policy router: {e}")

try:
    from app.api.routers.claims import router as claims_router
    app.include_router(claims_router)
except Exception as e:
    print(f"Warning: Could not load claims router: {e}")


@app.get("/")
def root():
    return {
        "message": "AI Insurance Platform Running"
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Insurance Policy Engine"
    }


# ============ FRONTEND COMPATIBILITY ENDPOINTS ============

class AskRequest(BaseModel):
    question: str


@app.post("/upload-policy")
async def upload_policy(file: UploadFile = File(...)):
    """Upload and ingest a PDF policy document"""
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        from app.infrastructure.pdf_parser import extract_text
        from app.infrastructure.text_chunker import chunk_text
        from app.services.vector_service import add_document
        
        UPLOAD_DIR = "data"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract and process
        pages = extract_text(file_path)
        if not pages:
            raise HTTPException(status_code=400, detail="No readable content found in PDF")

        # Store in vector DB
        for page in pages:
            if page["text"].strip():
                chunks = chunk_text(page["text"])
                for chunk in chunks:
                    add_document(
                        text=chunk,
                        metadata={
                            "source": file.filename,
                            "page": page["page"],
                        }
                    )

        return {"message": "Document ingested successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/ask")
async def ask_question(request: AskRequest):
    """Ask a question about the uploaded policy"""
    try:
        from app.services.rag_service import answer_question
        
        question = request.question
        session_id = str(uuid4())
        
        result = answer_question(question=question, session_id=session_id)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question processing failed: {str(e)}")
