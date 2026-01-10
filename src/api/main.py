"""
DocVerify AI - FastAPI Application

REST API endpoints for document verification.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import shutil
import os
import uuid
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List

from pydantic import BaseModel, Field

from src.core.config import get_settings
from src.core.logger import logger
from src.orchestration.processor import DocumentProcessor
from src.api import storage

settings = get_settings()

# Global Processor Instance
processor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager: Initialize processor on startup.
    """
    global processor
    logger.info("Startup: Initializing Document Processor...")
    try:
        processor = DocumentProcessor()
        logger.info("Startup: Processor ready")
    except Exception as e:
        logger.error("Startup Failed", error=str(e))

    yield

    logger.info("Shutdown: Cleanup...")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Document Verification API for Indian Government Documents",
    version="0.1.0",
    lifespan=lifespan
)

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydantic Models ---
class DocumentUploadResponse(BaseModel):
    document_id: str
    file_name: str
    file_size: int
    file_hash: str
    status: str
    message: str


class VerifyRequest(BaseModel):
    document_id: Optional[str] = None
    language_hint: Optional[str] = "en"
    document_type_hint: Optional[str] = None
    run_fraud_check: bool = True


class DocumentInfo(BaseModel):
    document_id: str
    file_name: str
    file_path: str
    file_hash: str
    file_size: int
    uploaded_at: str
    status: str


class OCRRequest(BaseModel):
    language_hint: Optional[str] = "en"
    preprocess: bool = True


class ClassifyRequest(BaseModel):
    ocr_text: str
    use_llm_fallback: bool = True


# --- Helper Functions ---
def compute_file_hash(file_path: str) -> str:
    """Compute SHA256 hash of file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


# --- Root & Health Endpoints ---
@app.get("/")
async def root():
    """API Information."""
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "description": "AI-Powered Document Verification Platform",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "upload": "/api/v1/documents/upload",
            "verify": "/api/v1/verify",
            "ocr": "/api/v1/ocr/extract",
            "classify": "/api/v1/classify"
        },
        "supported_documents": [
            "Aadhaar Card",
            "PAN Card",
            "Voter ID",
            "Driving License",
            "Passport",
            "Birth Certificate"
        ],
        "supported_languages": ["en", "hi", "ta", "te"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "online",
        "processor_initialized": processor is not None,
        "timestamp": datetime.utcnow().isoformat(),
        "database_enabled": settings.USE_DATABASE
    }


# --- Document Endpoints ---
@app.post("/api/v1/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    auto_verify: bool = Query(False, description="Automatically run verification after upload")
):
    """
    Upload a document for verification.

    Accepts PDF, PNG, JPG, JPEG, TIFF formats.
    Returns document ID for subsequent operations.
    """
    # Validate file type
    allowed_types = ["application/pdf", "image/png", "image/jpeg", "image/jpg", "image/tiff"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed: {allowed_types}"
        )

    try:
        document_id = str(uuid.uuid4())
        logger.info("Uploading document", document_id=document_id, filename=file.filename)

        # Create uploads directory
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{document_id}_{file.filename}"

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Compute hash
        file_hash = compute_file_hash(file_path)
        file_size = os.path.getsize(file_path)

        # Store document
        doc_info = {
            "document_id": document_id,
            "file_name": file.filename,
            "file_path": file_path,
            "file_hash": file_hash,
            "file_size": file_size,
            "mime_type": file.content_type,
            "uploaded_at": datetime.utcnow().isoformat(),
            "status": "uploaded"
        }
        await storage.save_document(doc_info)
        logger.info("Document uploaded", document_id=document_id)

        return DocumentUploadResponse(
            document_id=document_id,
            file_name=file.filename,
            file_size=file_size,
            file_hash=file_hash,
            status="uploaded",
            message="Document uploaded successfully. Use /api/v1/verify to verify."
        )

    except Exception as e:
        logger.error("Upload failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/documents")
async def list_documents(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """List uploaded documents."""
    docs = await storage.list_documents(limit=limit, offset=offset)
    return {"total": len(docs), "limit": limit, "offset": offset, "documents": docs}


@app.get("/api/v1/documents/{document_id}")
async def get_document(document_id: str):
    """Get document details by ID."""
    doc = await storage.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@app.delete("/api/v1/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document by ID."""
    doc = await storage.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete file
    file_path = doc.get("file_path")
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    await storage.delete_document(document_id)
    logger.info("Document deleted", document_id=document_id)
    return {"status": "deleted", "document_id": document_id}


# --- Verification Endpoints ---
@app.post("/api/v1/verify")
async def verify_document(
    file: Optional[UploadFile] = File(None),
    document_id: Optional[str] = Query(None, description="Document ID from previous upload")
):
    """
    Run verification on a document.

    Either provide a file directly or reference a previously uploaded document_id.
    """
    global processor
    if not processor:
        raise HTTPException(status_code=503, detail="Document Processor not initialized")

    try:
        verification_id = str(uuid.uuid4())
        file_path = None
        doc_id = None

        # Option 1: Direct file upload
        if file:
            doc_id = str(uuid.uuid4())
            os.makedirs("uploads", exist_ok=True)
            file_path = f"uploads/{doc_id}_{file.filename}"

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            logger.info("Received direct file for verification", verification_id=verification_id)

        # Option 2: Use existing document_id
        elif document_id:
            doc = await storage.get_document(document_id)
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")
            doc_id = document_id
            file_path = doc["file_path"]

        else:
            raise HTTPException(
                status_code=400,
                detail="Either provide a file or document_id"
            )

        logger.info("Starting verification", verification_id=verification_id, path=file_path)

        # Run Processing
        result = await processor.process(file_path)

        # Store verification
        verification = {
            "verification_id": verification_id,
            "document_id": doc_id,
            "verified_at": datetime.utcnow().isoformat(),
            **result
        }
        await storage.save_verification(verification)

        # Update document status
        status = "verified" if result.get("status") == "success" else "failed"
        await storage.update_document(doc_id, {"status": status})

        return verification

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Verification failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/verify/{verification_id}")
async def get_verification(verification_id: str):
    """Get verification result by ID."""
    ver = await storage.get_verification(verification_id)
    if not ver:
        raise HTTPException(status_code=404, detail="Verification not found")
    return ver


# --- Standalone OCR Endpoint ---
@app.post("/api/v1/ocr/extract")
async def ocr_extract(
    file: UploadFile = File(...),
    language_hint: str = Query("en", description="Language hint: en, hi, ta, te"),
    preprocess: bool = Query(True, description="Apply image preprocessing")
):
    """
    Standalone OCR extraction.

    Extract text from document without full verification pipeline.
    """
    global processor
    if not processor:
        raise HTTPException(status_code=503, detail="Processor not initialized")

    try:
        # Save temp file
        temp_id = str(uuid.uuid4())
        os.makedirs("uploads", exist_ok=True)
        temp_path = f"uploads/temp_{temp_id}_{file.filename}"

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Preprocess if requested
        if preprocess:
            processed_image = processor.preprocessor.process_path(temp_path)
        else:
            import cv2
            processed_image = cv2.imread(temp_path)

        # Run OCR
        text = processor.ocr.extract(processed_image)

        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return {
            "status": "success",
            "text": text,
            "language_hint": language_hint,
            "preprocessed": preprocess,
            "word_count": len(text.split()),
            "char_count": len(text)
        }

    except Exception as e:
        logger.error("OCR extraction failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# --- Standalone Classification Endpoint ---
@app.post("/api/v1/classify")
async def classify_document(request: ClassifyRequest):
    """
    Standalone document classification.

    Classify document type from OCR text without full verification.
    """
    global processor
    if not processor:
        raise HTTPException(status_code=503, detail="Processor not initialized")

    try:
        result = await processor.classifier.classify(request.ocr_text)

        return {
            "status": "success",
            "document_type": result.get("type", "unknown"),
            "confidence": result.get("confidence", 0.0),
            "method": result.get("method", "unknown"),
            "supported_types": [
                "aadhaar_card",
                "pan_card",
                "voter_id",
                "driving_license",
                "passport",
                "birth_certificate"
            ]
        }

    except Exception as e:
        logger.error("Classification failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# --- Analytics Endpoints ---
@app.get("/api/v1/analytics/summary")
async def analytics_summary():
    """Get verification analytics summary."""
    stats = await storage.get_stats()
    return stats


@app.get("/api/v1/analytics/accuracy")
async def analytics_accuracy():
    """Get accuracy metrics."""
    stats = await storage.get_stats()
    return {
        "total_verifications": stats.get("total_verifications", 0),
        "success_rate": stats.get("success_rate", 0),
        "database_enabled": settings.USE_DATABASE
    }
