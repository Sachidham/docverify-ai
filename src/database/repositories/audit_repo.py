"""
DocVerify AI - Audit Log Repository

Handles audit logging operations in Supabase.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime

from src.database.client import get_supabase
from src.database.models import AuditLog, AuditLogCreate
from src.core.logger import logger


class AuditRepository:
    """Repository for audit log operations."""

    TABLE_NAME = "audit_logs"

    def __init__(self):
        self.client = get_supabase()

    async def log(self, entry: AuditLogCreate) -> AuditLog:
        """Create a new audit log entry."""
        try:
            log_data = {
                "document_id": entry.document_id,
                "verification_id": entry.verification_id,
                "action": entry.action,
                "actor_id": entry.actor_id,
                "actor_type": entry.actor_type,
                "details": entry.details,
                "ip_address": entry.ip_address,
                "created_at": datetime.utcnow().isoformat()
            }

            result = self.client.table(self.TABLE_NAME).insert(log_data).execute()

            if result.data:
                return AuditLog(**result.data[0])

            raise Exception("Failed to create audit log")

        except Exception as e:
            # Don't raise - audit logging should never break the main flow
            logger.error("Failed to create audit log", error=str(e))
            return AuditLog(
                action=entry.action,
                document_id=entry.document_id,
                verification_id=entry.verification_id,
                details={"error": str(e)}
            )

    async def log_document_upload(
        self,
        document_id: str,
        file_name: str,
        file_hash: str,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log document upload action."""
        return await self.log(AuditLogCreate(
            document_id=document_id,
            action="document_uploaded",
            actor_type="system",
            details={
                "file_name": file_name,
                "file_hash": file_hash[:16] + "..."
            },
            ip_address=ip_address
        ))

    async def log_verification_started(
        self,
        document_id: str,
        verification_id: str,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log verification started action."""
        return await self.log(AuditLogCreate(
            document_id=document_id,
            verification_id=verification_id,
            action="verification_started",
            actor_type="system",
            ip_address=ip_address
        ))

    async def log_verification_completed(
        self,
        document_id: str,
        verification_id: str,
        status: str,
        confidence: float,
        processing_time_ms: int,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log verification completed action."""
        return await self.log(AuditLogCreate(
            document_id=document_id,
            verification_id=verification_id,
            action="verification_completed",
            actor_type="system",
            details={
                "status": status,
                "confidence": confidence,
                "processing_time_ms": processing_time_ms
            },
            ip_address=ip_address
        ))

    async def log_fraud_detected(
        self,
        document_id: str,
        verification_id: str,
        fraud_flags: List[Dict[str, Any]],
        tamper_score: float,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log fraud detection action."""
        return await self.log(AuditLogCreate(
            document_id=document_id,
            verification_id=verification_id,
            action="fraud_detected",
            actor_type="system",
            details={
                "fraud_flags": fraud_flags,
                "tamper_score": tamper_score
            },
            ip_address=ip_address
        ))

    async def log_document_deleted(
        self,
        document_id: str,
        actor_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log document deletion action."""
        return await self.log(AuditLogCreate(
            document_id=document_id,
            action="document_deleted",
            actor_id=actor_id,
            actor_type="user" if actor_id else "system",
            ip_address=ip_address
        ))

    async def log_manual_override(
        self,
        document_id: str,
        verification_id: str,
        actor_id: str,
        override_reason: str,
        new_status: str,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log manual verification override."""
        return await self.log(AuditLogCreate(
            document_id=document_id,
            verification_id=verification_id,
            action="manual_override",
            actor_id=actor_id,
            actor_type="user",
            details={
                "reason": override_reason,
                "new_status": new_status
            },
            ip_address=ip_address
        ))

    async def get_by_document_id(
        self,
        document_id: str,
        limit: int = 50
    ) -> List[AuditLog]:
        """Get audit logs for a document."""
        try:
            result = self.client.table(self.TABLE_NAME).select("*").eq("document_id", document_id).order("created_at", desc=True).limit(limit).execute()

            return [AuditLog(**log) for log in result.data]

        except Exception as e:
            logger.error("Failed to get audit logs", document_id=document_id, error=str(e))
            return []

    async def get_by_verification_id(
        self,
        verification_id: str
    ) -> List[AuditLog]:
        """Get audit logs for a verification."""
        try:
            result = self.client.table(self.TABLE_NAME).select("*").eq("verification_id", verification_id).order("created_at", desc=True).execute()

            return [AuditLog(**log) for log in result.data]

        except Exception as e:
            logger.error("Failed to get audit logs", verification_id=verification_id, error=str(e))
            return []

    async def list(
        self,
        limit: int = 100,
        offset: int = 0,
        action: Optional[str] = None
    ) -> List[AuditLog]:
        """List audit logs with pagination."""
        try:
            query = self.client.table(self.TABLE_NAME).select("*")

            if action:
                query = query.eq("action", action)

            query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
            result = query.execute()

            return [AuditLog(**log) for log in result.data]

        except Exception as e:
            logger.error("Failed to list audit logs", error=str(e))
            return []

    async def count(self, action: Optional[str] = None) -> int:
        """Count audit log entries."""
        try:
            query = self.client.table(self.TABLE_NAME).select("id", count="exact")

            if action:
                query = query.eq("action", action)

            result = query.execute()
            return result.count or 0

        except Exception as e:
            logger.error("Failed to count audit logs", error=str(e))
            return 0
