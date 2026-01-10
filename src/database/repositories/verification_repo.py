"""
DocVerify AI - Verification Repository

Handles CRUD operations for verifications in Supabase.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime

from src.database.client import get_supabase
from src.database.models import Verification, VerificationCreate, VerificationStatus
from src.core.logger import logger


class VerificationRepository:
    """Repository for verification operations."""

    TABLE_NAME = "verifications"

    def __init__(self):
        self.client = get_supabase()

    async def create(self, verification: VerificationCreate) -> Verification:
        """Create a new verification record."""
        try:
            ver_data = {
                "document_id": verification.document_id,
                "status": verification.status.value,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }

            result = self.client.table(self.TABLE_NAME).insert(ver_data).execute()

            if result.data:
                logger.info("Verification created", verification_id=result.data[0]["id"])
                return Verification(**result.data[0])

            raise Exception("Failed to create verification")

        except Exception as e:
            logger.error("Failed to create verification", error=str(e))
            raise

    async def get_by_id(self, verification_id: str) -> Optional[Verification]:
        """Get verification by ID."""
        try:
            result = self.client.table(self.TABLE_NAME).select("*").eq("id", verification_id).execute()

            if result.data:
                return Verification(**result.data[0])
            return None

        except Exception as e:
            logger.error("Failed to get verification", verification_id=verification_id, error=str(e))
            raise

    async def get_by_document_id(self, document_id: str) -> List[Verification]:
        """Get all verifications for a document."""
        try:
            result = self.client.table(self.TABLE_NAME).select("*").eq("document_id", document_id).order("created_at", desc=True).execute()

            return [Verification(**v) for v in result.data]

        except Exception as e:
            logger.error("Failed to get verifications for document", document_id=document_id, error=str(e))
            raise

    async def get_latest_by_document_id(self, document_id: str) -> Optional[Verification]:
        """Get the latest verification for a document."""
        try:
            result = self.client.table(self.TABLE_NAME).select("*").eq("document_id", document_id).order("created_at", desc=True).limit(1).execute()

            if result.data:
                return Verification(**result.data[0])
            return None

        except Exception as e:
            logger.error("Failed to get latest verification", document_id=document_id, error=str(e))
            raise

    async def list(
        self,
        limit: int = 10,
        offset: int = 0,
        status: Optional[VerificationStatus] = None
    ) -> List[Verification]:
        """List verifications with pagination."""
        try:
            query = self.client.table(self.TABLE_NAME).select("*")

            if status:
                query = query.eq("status", status.value)

            query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
            result = query.execute()

            return [Verification(**v) for v in result.data]

        except Exception as e:
            logger.error("Failed to list verifications", error=str(e))
            raise

    async def update(self, verification_id: str, updates: Dict[str, Any]) -> Optional[Verification]:
        """Update verification fields."""
        try:
            updates["updated_at"] = datetime.utcnow().isoformat()

            result = self.client.table(self.TABLE_NAME).update(updates).eq("id", verification_id).execute()

            if result.data:
                logger.info("Verification updated", verification_id=verification_id)
                return Verification(**result.data[0])
            return None

        except Exception as e:
            logger.error("Failed to update verification", verification_id=verification_id, error=str(e))
            raise

    async def update_status(
        self,
        verification_id: str,
        status: VerificationStatus,
        verified_by: Optional[str] = None
    ) -> Optional[Verification]:
        """Update verification status."""
        updates = {"status": status.value}

        if status == VerificationStatus.VERIFIED:
            updates["verified_at"] = datetime.utcnow().isoformat()
            if verified_by:
                updates["verified_by"] = verified_by

        return await self.update(verification_id, updates)

    async def update_results(
        self,
        verification_id: str,
        extracted_fields: Dict[str, Any],
        validation_results: Dict[str, Any],
        overall_confidence: float,
        processing_time_ms: int,
        ocr_engine: str = "paddleocr",
        llm_model: Optional[str] = None
    ) -> Optional[Verification]:
        """Update verification with processing results."""
        updates = {
            "extracted_fields": extracted_fields,
            "validation_results": validation_results,
            "overall_confidence": overall_confidence,
            "processing_time_ms": processing_time_ms,
            "ocr_engine_used": ocr_engine,
            "llm_model_used": llm_model,
            "status": VerificationStatus.VERIFIED.value if validation_results.get("is_valid") else VerificationStatus.REJECTED.value
        }

        if validation_results.get("is_valid"):
            updates["verified_at"] = datetime.utcnow().isoformat()

        return await self.update(verification_id, updates)

    async def update_fraud_check(
        self,
        verification_id: str,
        fraud_flags: List[Dict[str, Any]],
        tamper_score: float,
        duplicate_match_id: Optional[str] = None
    ) -> Optional[Verification]:
        """Update verification with fraud check results."""
        updates = {
            "fraud_flags": fraud_flags,
            "tamper_score": tamper_score,
            "duplicate_match_id": duplicate_match_id
        }

        # If high tamper score, flag for manual review
        if tamper_score > 0.5:
            updates["status"] = VerificationStatus.MANUAL_REVIEW.value

        return await self.update(verification_id, updates)

    async def update_detections(
        self,
        verification_id: str,
        stamps_detected: List[Dict[str, Any]],
        signatures_detected: List[Dict[str, Any]]
    ) -> Optional[Verification]:
        """Update verification with stamp/signature detections."""
        updates = {
            "stamps_detected": stamps_detected,
            "signatures_detected": signatures_detected
        }
        return await self.update(verification_id, updates)

    async def delete(self, verification_id: str) -> bool:
        """Delete a verification by ID."""
        try:
            self.client.table(self.TABLE_NAME).delete().eq("id", verification_id).execute()
            logger.info("Verification deleted", verification_id=verification_id)
            return True

        except Exception as e:
            logger.error("Failed to delete verification", verification_id=verification_id, error=str(e))
            raise

    async def count(self, status: Optional[VerificationStatus] = None) -> int:
        """Count verifications."""
        try:
            query = self.client.table(self.TABLE_NAME).select("id", count="exact")

            if status:
                query = query.eq("status", status.value)

            result = query.execute()
            return result.count or 0

        except Exception as e:
            logger.error("Failed to count verifications", error=str(e))
            return 0

    async def get_stats(self) -> Dict[str, Any]:
        """Get verification statistics."""
        try:
            total = await self.count()
            verified = await self.count(VerificationStatus.VERIFIED)
            rejected = await self.count(VerificationStatus.REJECTED)
            pending = await self.count(VerificationStatus.PENDING)
            manual_review = await self.count(VerificationStatus.MANUAL_REVIEW)

            return {
                "total": total,
                "verified": verified,
                "rejected": rejected,
                "pending": pending,
                "manual_review": manual_review,
                "success_rate": verified / total if total > 0 else 0
            }

        except Exception as e:
            logger.error("Failed to get stats", error=str(e))
            return {}
