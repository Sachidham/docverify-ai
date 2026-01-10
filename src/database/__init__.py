"""
DocVerify AI - Database Module

Supabase client and repositories for data persistence.
"""

from src.database.client import get_supabase, SupabaseManager
from src.database.models import (
    Document,
    DocumentCreate,
    DocumentType,
    Verification,
    VerificationCreate,
    VerificationStatus,
    AuditLog,
    AuditLogCreate,
    DocumentTemplate
)
from src.database.repositories import (
    DocumentRepository,
    VerificationRepository,
    AuditRepository
)

__all__ = [
    # Client
    "get_supabase",
    "SupabaseManager",
    # Models
    "Document",
    "DocumentCreate",
    "DocumentType",
    "Verification",
    "VerificationCreate",
    "VerificationStatus",
    "AuditLog",
    "AuditLogCreate",
    "DocumentTemplate",
    # Repositories
    "DocumentRepository",
    "VerificationRepository",
    "AuditRepository"
]
