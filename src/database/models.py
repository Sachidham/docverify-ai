"""
DocVerify AI - Database Models

Pydantic models for database entities.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from pydantic import BaseModel, Field
import uuid


class DocumentType(str, Enum):
    """Supported document types."""
    BIRTH_CERTIFICATE = "birth_certificate"
    AADHAAR_CARD = "aadhaar_card"
    PAN_CARD = "pan_card"
    DRIVING_LICENSE = "driving_license"
    VOTER_ID = "voter_id"
    PASSPORT = "passport"
    INCOME_CERTIFICATE = "income_certificate"
    CASTE_CERTIFICATE = "caste_certificate"
    DOMICILE_CERTIFICATE = "domicile_certificate"
    OTHER = "other"


class VerificationStatus(str, Enum):
    """Verification status states."""
    PENDING = "pending"
    PROCESSING = "processing"
    VERIFIED = "verified"
    REJECTED = "rejected"
    MANUAL_REVIEW = "manual_review"


class DocumentCreate(BaseModel):
    """Model for creating a new document."""
    file_name: str
    file_path: str
    file_hash: str
    mime_type: Optional[str] = None
    file_size_bytes: Optional[int] = None


class Document(BaseModel):
    """Document model matching database schema."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    file_name: str
    file_path: str
    file_hash: str
    mime_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    document_type: Optional[DocumentType] = None
    detected_language: Optional[str] = None
    raw_ocr_text: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None
    uploaded_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True


class VerificationCreate(BaseModel):
    """Model for creating a new verification."""
    document_id: str
    status: VerificationStatus = VerificationStatus.PENDING


class Verification(BaseModel):
    """Verification model matching database schema."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str
    status: VerificationStatus = VerificationStatus.PENDING
    overall_confidence: Optional[float] = None
    extracted_fields: Optional[Dict[str, Any]] = None
    field_confidences: Optional[Dict[str, float]] = None
    validation_results: Optional[Dict[str, Any]] = None
    stamps_detected: Optional[List[Dict[str, Any]]] = None
    signatures_detected: Optional[List[Dict[str, Any]]] = None
    fraud_flags: Optional[List[Dict[str, Any]]] = None
    tamper_score: Optional[float] = None
    duplicate_match_id: Optional[str] = None
    processing_time_ms: Optional[int] = None
    ocr_engine_used: Optional[str] = None
    llm_model_used: Optional[str] = None
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True


class AuditLogCreate(BaseModel):
    """Model for creating an audit log entry."""
    document_id: Optional[str] = None
    verification_id: Optional[str] = None
    action: str
    actor_id: Optional[str] = None
    actor_type: Optional[str] = "system"
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None


class AuditLog(BaseModel):
    """Audit log model matching database schema."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    document_id: Optional[str] = None
    verification_id: Optional[str] = None
    action: str
    actor_id: Optional[str] = None
    actor_type: Optional[str] = "system"
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True


class DocumentTemplate(BaseModel):
    """Document template model for validation rules."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    document_type: DocumentType
    template_name: str
    language: Optional[str] = None
    region: Optional[str] = None
    field_schema: Dict[str, Any]
    validation_rules: Optional[Dict[str, Any]] = None
    layout_hints: Optional[Dict[str, Any]] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
