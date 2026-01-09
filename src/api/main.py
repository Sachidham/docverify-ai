from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import shutil
import os
import uuid
from typing import Dict, Any

from src.core.config import get_settings
from src.core.logger import logger
from src.orchestration.agent_manager import AgentManager
from src.orchestration.agents import OCRAgent, ClassificationAgent, ExtractionAgent

settings = get_settings()

# Global Agent Manager
agent_manager = AgentManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager: Initialize agents on startup, shutdown on exit.
    """
    logger.info("Startup: Initializing Agent Manager...")
    
    # Register core agents
    agent_manager.register_agent_type("ocr", OCRAgent)
    agent_manager.register_agent_type("classification", ClassificationAgent)
    agent_manager.register_agent_type("extraction", ExtractionAgent)
    
    # Pre-spawn workers (warmup)
    await agent_manager.spawn_agent("ocr", {"engine": settings.DEFAULT_OCR_ENGINE})
    await agent_manager.spawn_agent("classification", {})
    await agent_manager.spawn_agent("extraction", {})
    
    logger.info("Startup: Agents ready")
    
    yield
    
    logger.info("Shutdown: Terminating agents...")
    await agent_manager.shutdown_all()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Document Verification API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS (Allow Streamlit)
origins = [
    "http://localhost:8501",
    "http://localhost:3000",
    "*" # For dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "agents": agent_manager.list_active_agents()
    }

@app.post("/api/v1/verify")
async def verify_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Main verification endpoint.
    Accepts a file, saves it, and runs the verification pipeline.
    """
    try:
        request_id = str(uuid.uuid4())
        logger.info("Received verification request", request_id=request_id, filename=file.filename)
        
        # 1. Save file locally (simulation of storage)
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{request_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info("File saved", path=file_path)

        # 2. Trigger Agents (Mock Pipeline for now)
        # In real implementation, we would orchestrate this properly
        # For now, we just return a success signal with mock data
        
        return {
            "verification_id": request_id, 
            "status": "processing",
            "message": "Document received and processing started",
            "mock_result": {
                "document_type": "aadhaar_card",
                "extracted_fields": {
                    "name": "Mock User",
                    "id": "1234-5678-9012"
                },
                "verification_status": "pending_validation"
            }
        }
        
    except Exception as e:
        logger.error("Verification failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
