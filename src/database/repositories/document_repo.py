"""
DocVerify AI - Document Repository

Handles CRUD operations for documents in Supabase.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime

from src.database.client import get_supabase
from src.database.models import Document, DocumentCreate, DocumentType
from src.core.logger import logger


class DocumentRepository:
    """Repository for document operations."""

    TABLE_NAME = "documents"

    def __init__(self):
        self.client = get_supabase()

    async def create(self, document: DocumentCreate) -> Document:
        """Create a new document record."""
        try:
            doc_data = {
                "file_name": document.file_name,
                "file_path": document.file_path,
                "file_hash": document.file_hash,
                "mime_type": document.mime_type,
                "file_size_bytes": document.file_size_bytes,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }

            result = self.client.table(self.TABLE_NAME).insert(doc_data).execute()

            if result.data:
                logger.info("Document created", document_id=result.data[0]["id"])
                return Document(**result.data[0])

            raise Exception("Failed to create document")

        except Exception as e:
            logger.error("Failed to create document", error=str(e))
            raise

    async def get_by_id(self, document_id: str) -> Optional[Document]:
        """Get document by ID."""
        try:
            result = self.client.table(self.TABLE_NAME).select("*").eq("id", document_id).execute()

            if result.data:
                return Document(**result.data[0])
            return None

        except Exception as e:
            logger.error("Failed to get document", document_id=document_id, error=str(e))
            raise

    async def get_by_hash(self, file_hash: str) -> Optional[Document]:
        """Get document by file hash (for duplicate detection)."""
        try:
            result = self.client.table(self.TABLE_NAME).select("*").eq("file_hash", file_hash).execute()

            if result.data:
                return Document(**result.data[0])
            return None

        except Exception as e:
            logger.error("Failed to get document by hash", error=str(e))
            raise

    async def list(
        self,
        limit: int = 10,
        offset: int = 0,
        document_type: Optional[DocumentType] = None
    ) -> List[Document]:
        """List documents with pagination."""
        try:
            query = self.client.table(self.TABLE_NAME).select("*")

            if document_type:
                query = query.eq("document_type", document_type.value)

            query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
            result = query.execute()

            return [Document(**doc) for doc in result.data]

        except Exception as e:
            logger.error("Failed to list documents", error=str(e))
            raise

    async def update(self, document_id: str, updates: Dict[str, Any]) -> Optional[Document]:
        """Update document fields."""
        try:
            updates["updated_at"] = datetime.utcnow().isoformat()

            result = self.client.table(self.TABLE_NAME).update(updates).eq("id", document_id).execute()

            if result.data:
                logger.info("Document updated", document_id=document_id)
                return Document(**result.data[0])
            return None

        except Exception as e:
            logger.error("Failed to update document", document_id=document_id, error=str(e))
            raise

    async def update_ocr_result(
        self,
        document_id: str,
        ocr_text: str,
        detected_language: Optional[str] = None
    ) -> Optional[Document]:
        """Update document with OCR results."""
        updates = {
            "raw_ocr_text": ocr_text,
            "detected_language": detected_language
        }
        return await self.update(document_id, updates)

    async def update_classification(
        self,
        document_id: str,
        document_type: DocumentType,
        structured_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Document]:
        """Update document with classification results."""
        updates = {
            "document_type": document_type.value,
            "structured_data": structured_data
        }
        return await self.update(document_id, updates)

    async def delete(self, document_id: str) -> bool:
        """Delete a document by ID."""
        try:
            result = self.client.table(self.TABLE_NAME).delete().eq("id", document_id).execute()
            logger.info("Document deleted", document_id=document_id)
            return True

        except Exception as e:
            logger.error("Failed to delete document", document_id=document_id, error=str(e))
            raise

    async def count(self, document_type: Optional[DocumentType] = None) -> int:
        """Count documents."""
        try:
            query = self.client.table(self.TABLE_NAME).select("id", count="exact")

            if document_type:
                query = query.eq("document_type", document_type.value)

            result = query.execute()
            return result.count or 0

        except Exception as e:
            logger.error("Failed to count documents", error=str(e))
            return 0

    async def find_duplicates(self, file_hash: str, exclude_id: Optional[str] = None) -> List[Document]:
        """Find documents with the same file hash."""
        try:
            query = self.client.table(self.TABLE_NAME).select("*").eq("file_hash", file_hash)

            if exclude_id:
                query = query.neq("id", exclude_id)

            result = query.execute()
            return [Document(**doc) for doc in result.data]

        except Exception as e:
            logger.error("Failed to find duplicates", error=str(e))
            return []
