"""
Storage abstraction - uses Supabase if configured, else in-memory.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from src.core.config import get_settings
from src.core.logger import logger

settings = get_settings()

# In-memory fallback
_docs_memory: Dict[str, Dict] = {}
_verifications_memory: Dict[str, Dict] = {}

# Database repos (lazy loaded)
_doc_repo = None
_ver_repo = None
_audit_repo = None


def _get_repos():
    """Lazy load repos if DB enabled."""
    global _doc_repo, _ver_repo, _audit_repo
    if settings.USE_DATABASE and settings.SUPABASE_URL:
        if _doc_repo is None:
            from src.database.repositories import DocumentRepository, VerificationRepository, AuditRepository
            _doc_repo = DocumentRepository()
            _ver_repo = VerificationRepository()
            _audit_repo = AuditRepository()
            logger.info("Database storage enabled")
    return _doc_repo, _ver_repo, _audit_repo


# --- Document Storage ---

async def save_document(doc: Dict) -> str:
    """Save document, returns doc_id."""
    doc_id = doc.get("document_id")
    doc_repo, _, audit_repo = _get_repos()

    if doc_repo:
        try:
            from src.database.models import DocumentCreate
            db_doc = await doc_repo.create(DocumentCreate(
                file_name=doc["file_name"],
                file_path=doc["file_path"],
                file_hash=doc["file_hash"],
                mime_type=doc.get("mime_type"),
                file_size_bytes=doc.get("file_size")
            ))
            if audit_repo:
                await audit_repo.log_document_upload(db_doc.id, doc["file_name"], doc["file_hash"])
            return db_doc.id
        except Exception as e:
            logger.warning("DB save failed, using memory", error=str(e))

    # Fallback to memory
    _docs_memory[doc_id] = doc
    return doc_id


async def get_document(doc_id: str) -> Optional[Dict]:
    """Get document by ID."""
    doc_repo, _, _ = _get_repos()

    if doc_repo:
        try:
            doc = await doc_repo.get_by_id(doc_id)
            if doc:
                return doc.model_dump()
        except Exception as e:
            logger.warning("DB get failed", error=str(e))

    return _docs_memory.get(doc_id)


async def list_documents(limit: int = 10, offset: int = 0) -> List[Dict]:
    """List documents."""
    doc_repo, _, _ = _get_repos()

    if doc_repo:
        try:
            docs = await doc_repo.list(limit=limit, offset=offset)
            return [d.model_dump() for d in docs]
        except Exception as e:
            logger.warning("DB list failed", error=str(e))

    docs = list(_docs_memory.values())
    return docs[offset:offset + limit]


async def delete_document(doc_id: str) -> bool:
    """Delete document."""
    doc_repo, _, _ = _get_repos()

    if doc_repo:
        try:
            await doc_repo.delete(doc_id)
            return True
        except Exception as e:
            logger.warning("DB delete failed", error=str(e))

    if doc_id in _docs_memory:
        del _docs_memory[doc_id]
        return True
    return False


async def update_document(doc_id: str, updates: Dict) -> None:
    """Update document fields."""
    doc_repo, _, _ = _get_repos()

    if doc_repo:
        try:
            await doc_repo.update(doc_id, updates)
            return
        except Exception as e:
            logger.warning("DB update failed", error=str(e))

    if doc_id in _docs_memory:
        _docs_memory[doc_id].update(updates)


# --- Verification Storage ---

async def save_verification(ver: Dict) -> str:
    """Save verification, returns ver_id."""
    ver_id = ver.get("verification_id")
    _, ver_repo, audit_repo = _get_repos()

    if ver_repo:
        try:
            from src.database.models import VerificationCreate
            db_ver = await ver_repo.create(VerificationCreate(
                document_id=ver["document_id"]
            ))
            # Update with full results
            await ver_repo.update(db_ver.id, {
                "extracted_fields": ver.get("extracted_fields"),
                "validation_results": ver.get("validation"),
                "overall_confidence": ver.get("confidence"),
                "status": "verified" if ver.get("validation", {}).get("is_valid") else "rejected"
            })
            if audit_repo:
                await audit_repo.log_verification_completed(
                    ver["document_id"], db_ver.id,
                    ver.get("status", "unknown"),
                    ver.get("confidence", 0), 0
                )
            return db_ver.id
        except Exception as e:
            logger.warning("DB save verification failed", error=str(e))

    _verifications_memory[ver_id] = ver
    return ver_id


async def get_verification(ver_id: str) -> Optional[Dict]:
    """Get verification by ID."""
    _, ver_repo, _ = _get_repos()

    if ver_repo:
        try:
            ver = await ver_repo.get_by_id(ver_id)
            if ver:
                return ver.model_dump()
        except Exception as e:
            logger.warning("DB get verification failed", error=str(e))

    return _verifications_memory.get(ver_id)


async def get_stats() -> Dict[str, Any]:
    """Get verification stats."""
    _, ver_repo, _ = _get_repos()

    if ver_repo:
        try:
            return await ver_repo.get_stats()
        except Exception as e:
            logger.warning("DB stats failed", error=str(e))

    # In-memory stats
    total = len(_verifications_memory)
    success = sum(1 for v in _verifications_memory.values() if v.get("status") == "success")
    return {
        "total_documents": len(_docs_memory),
        "total_verifications": total,
        "verified_successfully": success,
        "success_rate": success / total if total > 0 else 0
    }
