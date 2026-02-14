from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from app.infrastructure.pdf_parser import extract_text
from app.infrastructure.text_chunker import chunk_text
from app.services.vector_service import add_document

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingests a PDF document:
    - Saves file
    - Extracts text (with OCR fallback)
    - Splits into overlapping chunks
    - Stores chunks in vector database
    """

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_text(file_path)

    if not pages:
        raise HTTPException(status_code=400, detail="No readable content found in PDF.")

    total_chunks = 0

    for page in pages:
        if page["text"].strip():
            chunks = chunk_text(page["text"])

            for i, chunk in enumerate(chunks):
                add_document(
                    text=chunk,
                    metadata={
                        "source": file.filename,
                        "page": page["page"],
                        "chunk": i
                    }
                )
                total_chunks += 1

    return {
        "message": "Document ingested successfully",
        "pages_processed": len(pages),
        "chunks_created": total_chunks
    }
