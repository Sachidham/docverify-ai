# 📋 DocVerify AI - Product Requirements Document (PRD)

## AI-Powered Document Verification Platform for Indian Government Services

**Version:** 1.0  
**Created:** January 2025  
**Status:** In Development  
**Timeline:** 15 Days Sprint  

---

# Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Context & Background](#2-project-context--background)
3. [Design Decisions & Rationale](#3-design-decisions--rationale)
4. [Technical Architecture](#4-technical-architecture)
5. [Tech Stack Specification](#5-tech-stack-specification)
6. [Feature Requirements](#6-feature-requirements)
7. [Database Schema](#7-database-schema)
8. [API Specification](#8-api-specification)
9. [MCP Server Specification](#9-mcp-server-specification)
10. [Project Structure](#10-project-structure)
11. [15-Day Development Roadmap](#11-15-day-development-roadmap)
12. [Module Specifications](#12-module-specifications)
13. [Success Metrics](#13-success-metrics)
14. [MVP Scope](#14-mvp-scope)
15. [Setup Instructions](#15-setup-instructions)
16. [Quick Reference](#16-quick-reference)

---

# 1. Executive Summary

## 1.1 Problem Statement

Indian government services require verification of citizen-submitted documents (birth certificates, IDs, licenses, income declarations, etc.). Currently, this process is:
- Manual and time-consuming
- Prone to human error
- Difficult to scale
- Vulnerable to fraud

## 1.2 Solution

**DocVerify AI** is an AI-powered document verification platform that automates the entire verification pipeline using:
- Multi-language OCR (Hindi, English, Tamil, Telugu)
- LLM-powered classification and extraction
- Rule-based and AI-driven validation
- Fraud detection via embeddings and visual analysis
- MCP server for tool integration with AI assistants

## 1.3 Key Metrics

| Metric | Value |
|--------|-------|
| **Timeline** | 15 days |
| **Team Size** | 2 developers |
| **API Cost** | $0 (Free tier only) |
| **Languages Supported** | 4 (Tier 1: Hindi, English, Tamil, Telugu) |
| **Document Types** | 5+ (expandable) |

---

# 2. Project Context & Background

## 2.1 Original Requirements

The platform must provide these **8 Core Capabilities**:

1. **Accurate Digitization** - Fine-tuned OCR for multiple Indian languages
2. **Noisy Input Preprocessing** - De-skewing, noise removal, contrast enhancement
3. **Document Type Classification** - Auto-identify document categories
4. **Key Field Extraction & Validation** - Names, dates, IDs, addresses
5. **Stamp and Signature Detection** - Official seal verification
6. **Fraud and Tamper Detection** - Identify manipulated documents
7. **Offline/Edge Support** - (Deferred to post-MVP)
8. **System Integration** - APIs and MCP tools for service delivery

## 2.2 Success Criteria

- Institutional adoption at scale
- Reduced verification time (target: <10 seconds)
- Improved OCR accuracy for regional languages (target: 85%+)
- Early fraud detection (target: 80% recall)
- Explainable and auditable results

## 2.3 Constraints

- **Budget:** Very tight, zero API cost preferred
- **Team:** 2 people, intermediate Python, beginner ML/CV
- **Timeline:** 15 days (aggressive, AI-assisted development)
- **Infrastructure:** Local GPU + Jarvis Labs/Antigravity credits

---

# 3. Design Decisions & Rationale

## 3.1 LLM Strategy

### Decision: Gemini 2.0 Flash (Free) + Ollama (Local)

**Why NOT Anthropic API:**
- Anthropic API is paid only (no free tier)
- Budget constraint is critical

**Why Gemini:**
- Free tier: 1,500 requests/day, 15 req/minute
- Excellent reasoning and vision capabilities
- Vision model included (same API)

**Why Ollama:**
- Completely free (runs locally)
- Uses available GPU on Antigravity
- Good for high-volume tasks (embeddings, simple extraction)

| Use Case | Model | Cost |
|----------|-------|------|
| Complex reasoning | Gemini 2.0 Flash | Free |
| Vision/classification | Gemini 2.0 Flash | Free |
| High-volume OCR enhancement | Ollama + Llama 3.1 8B | Free |
| Embeddings | Ollama + nomic-embed-text | Free |
| Local vision (backup) | Ollama + LLaVA 7B | Free |

## 3.2 Language Support

### Decision: Tier 1 Languages First

**Tier 1 (MVP):**
- English (en)
- Hindi (hi) - Devanagari script
- Tamil (ta) - Tamil script
- Telugu (te) - Telugu script

**Tier 2 (Post-MVP):**
- Bengali, Kannada, Malayalam, Marathi, Gujarati

**Tier 3 (Future):**
- Odia, Punjabi, Assamese, others

**Rationale:** Tier 1 covers largest population segments and PaddleOCR has strong support for these.

## 3.3 Framework Choices

### Decision: Use BOTH LangChain AND LlamaIndex

**LangChain for:**
- Agent orchestration
- Tool calling
- Chain composition
- Multi-step reasoning

**LlamaIndex for:**
- Document processing
- RAG (Retrieval Augmented Generation)
- Template knowledge base
- Embedding management

**Rationale:** They complement each other well. LlamaIndex excels at document handling, LangChain at orchestration.

## 3.4 Database Choice

### Decision: Supabase (All-in-One)

Using Supabase for:
- ✅ **PostgreSQL** - Metadata storage
- ✅ **pgvector** - Embeddings for duplicate detection
- ✅ **Storage** - Document file storage
- ✅ **Auth** - User management (future)
- ✅ **Realtime** - Live updates (future)

**Rationale:** Single platform, generous free tier, easy setup, pgvector built-in.

## 3.5 OCR Strategy

### Decision: Multi-Engine Ensemble

**Primary: PaddleOCR**
- Best accuracy for Indian languages
- Active development
- GPU accelerated

**Fallback: EasyOCR**
- Good multi-language support
- Different error patterns (good for ensemble)

**Backup: Tesseract 5**
- Industry standard
- Indic language packs available

**Ensemble Strategy:**
- Run multiple engines
- Select result with highest confidence
- (Future: voting-based fusion)

## 3.6 MCP Integration

### Decision: Build MCP Server from Day 1

**Why MCP:**
- Expose verification tools to Claude Desktop/other AI assistants
- Standardized tool interface
- Future-proof architecture
- Enables integration with other MCP-compatible clients

**Transport:** Streamable HTTP (for remote access)

## 3.7 UI Choice

### Decision: Streamlit

**Why Streamlit:**
- Fastest to build (Python-native)
- Team knows Python (not React)
- Professional enough for demo
- Built-in components for ML/data apps
- 15-day timeline constraint

**Alternatives Considered:**
- Gradio: Even simpler, but less customizable
- React: Better UI, but longer development time

## 3.8 Team Division

### Decision: Module-Based Split

**Developer A (You):**
- Backend architecture
- OCR engines
- LLM integration
- MCP Server
- Pipeline orchestration

**Developer B (Teammate):**
- Database/Supabase
- Image preprocessing
- Streamlit UI
- Validation rules
- Testing

---

# 4. Technical Architecture

## 4.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DOCVERIFY AI PLATFORM                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   STREAMLIT  │    │   FASTAPI    │    │  MCP SERVER  │                  │
│  │   Dashboard  │───▶│   REST API   │◀───│   (Tools)    │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│         │                   │                   │                           │
│         └───────────────────┼───────────────────┘                           │
│                             ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     ORCHESTRATION LAYER                               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                   │  │
│  │  │ LangChain   │  │ LlamaIndex  │  │   Agents    │                   │  │
│  │  │ Chains      │  │ Document    │  │  & Tools    │                   │  │
│  │  │ & Agents    │  │ Processing  │  │  Registry   │                   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                             │                                               │
│                             ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      PROCESSING MODULES                               │  │
│  │                                                                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │
│  │  │  Image   │ │   OCR    │ │ Document │ │  Field   │ │  Fraud   │   │  │
│  │  │ Preproc  │ │  Engine  │ │ Classify │ │ Extract  │ │ Detect   │   │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘   │  │
│  │       │            │            │            │            │          │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │
│  │  │  Stamp   │ │Signature │ │  Layout  │ │Validation│ │  Audit   │   │  │
│  │  │ Detect   │ │ Verify   │ │ Analysis │ │  Rules   │ │  Logger  │   │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                             │                                               │
│                             ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         LLM LAYER                                     │  │
│  │  ┌────────────────────┐        ┌────────────────────┐                │  │
│  │  │   Gemini 2.0 Flash │        │   Ollama (Local)   │                │  │
│  │  │   - Reasoning      │        │   - Llama 3.1 8B   │                │  │
│  │  │   - Vision         │        │   - Qwen2.5 7B     │                │  │
│  │  │   - Validation     │        │   - nomic-embed    │                │  │
│  │  └────────────────────┘        └────────────────────┘                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                             │                                               │
│                             ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        SUPABASE                                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│  │  │PostgreSQL│  │ pgvector │  │ Storage  │  │   Auth   │             │  │
│  │  │ Metadata │  │Embeddings│  │  Files   │  │  Users   │             │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4.2 Data Flow

```
┌─────────┐    ┌─────────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐
│ Upload  │───▶│ Preprocess  │───▶│   OCR   │───▶│ Classify │───▶│ Extract  │
│Document │    │ (deskew,    │    │(Paddle/ │    │(LLM+     │    │ Fields   │
│         │    │  denoise)   │    │ Easy)   │    │template) │    │          │
└─────────┘    └─────────────┘    └─────────┘    └──────────┘    └──────────┘
                                                                       │
┌─────────┐    ┌─────────────┐    ┌─────────┐    ┌──────────┐          │
│ Return  │◀───│   Fraud     │◀───│ Detect  │◀───│ Validate │◀─────────┘
│ Result  │    │   Check     │    │ Stamps  │    │ Fields   │
│         │    │             │    │         │    │          │
└─────────┘    └─────────────┘    └─────────┘    └──────────┘
```

---

# 5. Tech Stack Specification

## 5.1 Core Framework

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | Python | 3.11+ | Primary development language |
| API Framework | FastAPI | 0.115+ | REST API endpoints |
| UI Framework | Streamlit | 1.40+ | Dashboard interface |
| Package Manager | Poetry | 1.8+ | Dependency management |

## 5.2 LLM & AI

| Component | Technology | Cost | Purpose |
|-----------|------------|------|---------|
| Primary LLM | Google Gemini 2.0 Flash | Free | Reasoning, validation |
| Local LLM | Ollama + Llama 3.1 8B | Free | High-volume tasks |
| Vision Model | Gemini 2.0 Flash Vision | Free | Document analysis |
| Embeddings | Ollama + nomic-embed-text | Free | Duplicate detection |
| Orchestration | LangChain 0.3+ | Free | Agent management |
| Document RAG | LlamaIndex 0.11+ | Free | Document processing |

## 5.3 OCR & Vision

| Component | Technology | Languages |
|-----------|------------|-----------|
| Primary OCR | PaddleOCR 2.8+ | Hindi, Tamil, Telugu, English |
| Fallback OCR | EasyOCR 1.7+ | Multi-language support |
| Backup OCR | Tesseract 5.0 | With Indic language packs |
| Image Processing | OpenCV 4.10+ | Preprocessing |
| PDF Processing | PyMuPDF 1.24+ | PDF handling |

## 5.4 Database

| Component | Technology | Purpose |
|-----------|------------|---------|
| Database | Supabase PostgreSQL | Metadata, audit logs |
| Vector Store | pgvector | Embeddings for similarity |
| File Storage | Supabase Storage | Document files |
| Auth | Supabase Auth | User management (future) |

## 5.5 MCP Server

| Component | Technology | Purpose |
|-----------|------------|---------|
| MCP Framework | mcp-python-sdk (FastMCP) | Tool server |
| Validation | Pydantic v2 | Input/output validation |
| Transport | Streamable HTTP | Remote access |

## 5.6 Complete Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.11"

# Web Framework
fastapi = "^0.115.0"
uvicorn = {extras = ["standard"], version = "^0.32.0"}
python-multipart = "^0.0.12"

# UI
streamlit = "^1.40.0"

# Database
supabase = "^2.10.0"
sqlalchemy = "^2.0.0"
asyncpg = "^0.30.0"
pgvector = "^0.3.0"

# LLM & AI
langchain = "^0.3.7"
langchain-google-genai = "^2.0.0"
langchain-community = "^0.3.5"
llama-index = "^0.11.0"
llama-index-llms-ollama = "^0.4.0"
llama-index-embeddings-ollama = "^0.4.0"
google-generativeai = "^0.8.0"
ollama = "^0.4.0"

# OCR
paddleocr = "^2.8.0"
paddlepaddle = "^2.6.0"
easyocr = "^1.7.0"
pytesseract = "^0.3.10"

# Image Processing
opencv-python = "^4.10.0"
Pillow = "^11.0.0"
scikit-image = "^0.24.0"

# PDF Processing  
PyMuPDF = "^1.24.0"
img2table = "^1.3.0"

# Layout Analysis
layoutparser = "^0.3.4"

# MCP Server
mcp = "^1.0.0"

# Utilities
pydantic = "^2.9.0"
pydantic-settings = "^2.6.0"
python-dotenv = "^1.0.0"
httpx = "^0.28.0"
numpy = "^1.26.0"
pandas = "^2.2.0"
structlog = "^24.4.0"

# Synthetic Data
Faker = "^30.0.0"
reportlab = "^4.2.0"
```

---

# 6. Feature Requirements

## 6.1 Core Features (MVP)

### F1: Document Upload
- Accept PDF, PNG, JPG, JPEG, TIFF
- Max file size: 20MB
- Store in Supabase Storage
- Calculate file hash for deduplication

### F2: Image Preprocessing
- Auto-deskew (correct rotation)
- Noise removal (Gaussian, median filters)
- Contrast enhancement (CLAHE)
- Resolution normalization (300 DPI)

### F3: Multi-Language OCR
- Support: English, Hindi, Tamil, Telugu
- Confidence scoring per word
- Bounding box extraction
- Ensemble voting for accuracy

### F4: Document Classification
- Auto-detect document type
- Supported types:
  - Aadhaar Card
  - PAN Card
  - Birth Certificate
  - Driving License
  - Voter ID
  - Income Certificate
  - Other
- Confidence score with reasoning

### F5: Field Extraction
- Document-specific field extraction
- Supported fields by document:
  - **Aadhaar:** Name, Number, DOB, Gender, Address
  - **PAN:** Name, Number, Father's Name, DOB
  - **Birth Certificate:** Name, DOB, Place, Parents
  - **Driving License:** Name, Number, DOB, Validity, Classes
- Multi-source extraction (regex + NER + LLM)

### F6: Field Validation
- Format validation (checksum, patterns)
- Logical validation (date ranges, consistency)
- Cross-field validation
- LLM-assisted validation

### F7: Stamp & Signature Detection
- Detect official stamps/seals
- Detect handwritten signatures
- Position validation against templates
- Confidence scoring

### F8: Basic Fraud Detection
- Duplicate detection (embedding similarity)
- Layout consistency check
- Basic tamper detection
- Risk scoring (low/medium/high)

### F9: MCP Server
- Expose all capabilities as MCP tools
- Tools:
  - `docverify_ocr_extract`
  - `docverify_classify_document`
  - `docverify_extract_fields`
  - `docverify_validate_fields`
  - `docverify_check_fraud`
  - `docverify_detect_stamps`
  - `docverify_full_verification`

### F10: Dashboard UI
- Document upload interface
- Verification status display
- Field-by-field results
- Confidence meters
- Fraud alerts
- Basic analytics

## 6.2 Deferred Features (Post-MVP)

- Offline/edge deployment
- Advanced fraud ML models
- Physical document scanning
- Full authentication & RBAC
- Multi-tenant support
- Advanced analytics & reporting
- Batch processing queue
- Webhook integrations

---

# 7. Database Schema

## 7.1 SQL Schema

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Document Types Enum
CREATE TYPE document_type AS ENUM (
    'birth_certificate',
    'aadhaar_card', 
    'pan_card',
    'driving_license',
    'voter_id',
    'passport',
    'income_certificate',
    'caste_certificate',
    'domicile_certificate',
    'other'
);

-- Verification Status Enum
CREATE TYPE verification_status AS ENUM (
    'pending',
    'processing', 
    'verified',
    'rejected',
    'manual_review'
);

-- Documents Table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    mime_type VARCHAR(100),
    file_size_bytes INTEGER,
    
    document_type document_type,
    detected_language VARCHAR(50),
    
    raw_ocr_text TEXT,
    structured_data JSONB,
    
    embedding vector(768),
    
    uploaded_by UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Verifications Table
CREATE TABLE verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    
    status verification_status DEFAULT 'pending',
    overall_confidence DECIMAL(5,4),
    
    extracted_fields JSONB,
    field_confidences JSONB,
    validation_results JSONB,
    
    stamps_detected JSONB,
    signatures_detected JSONB,
    
    fraud_flags JSONB,
    tamper_score DECIMAL(5,4),
    duplicate_match_id UUID,
    
    processing_time_ms INTEGER,
    ocr_engine_used VARCHAR(50),
    llm_model_used VARCHAR(100),
    
    verified_by UUID,
    verified_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit Logs Table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id),
    verification_id UUID REFERENCES verifications(id),
    
    action VARCHAR(100) NOT NULL,
    actor_id UUID,
    actor_type VARCHAR(50),
    
    details JSONB,
    ip_address INET,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Document Templates Table
CREATE TABLE document_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_type document_type NOT NULL,
    
    template_name VARCHAR(255) NOT NULL,
    language VARCHAR(50),
    region VARCHAR(100),
    
    field_schema JSONB NOT NULL,
    validation_rules JSONB,
    layout_hints JSONB,
    
    sample_embedding vector(768),
    
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_hash ON documents(file_hash);
CREATE INDEX idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_verifications_status ON verifications(status);
CREATE INDEX idx_verifications_document ON verifications(document_id);
CREATE INDEX idx_audit_document ON audit_logs(document_id);
```

## 7.2 Entity Relationship

```
┌─────────────┐       ┌─────────────────┐       ┌─────────────┐
│  documents  │──────▶│  verifications  │──────▶│ audit_logs  │
└─────────────┘       └─────────────────┘       └─────────────┘
       │                                               │
       │              ┌─────────────────┐              │
       └─────────────▶│document_templates│◀────────────┘
                      └─────────────────┘
```

---

# 8. API Specification

## 8.1 Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/api/v1/documents/upload` | Upload document |
| GET | `/api/v1/documents` | List documents |
| GET | `/api/v1/documents/{id}` | Get document |
| DELETE | `/api/v1/documents/{id}` | Delete document |
| POST | `/api/v1/verify` | Run verification |
| GET | `/api/v1/verify/{id}` | Get verification |
| POST | `/api/v1/verify/override` | Manual override |
| POST | `/api/v1/ocr/extract` | Standalone OCR |
| POST | `/api/v1/classify` | Standalone classification |
| GET | `/api/v1/analytics/summary` | Analytics summary |
| GET | `/api/v1/analytics/accuracy` | Accuracy metrics |

## 8.2 Key Request/Response Examples

### Upload Document
```http
POST /api/v1/documents/upload
Content-Type: multipart/form-data

file: <binary>
auto_verify: true
language_hint: hi
```

```json
{
  "document_id": "doc_abc123",
  "file_name": "aadhaar.pdf",
  "file_size": 245678,
  "status": "uploaded",
  "message": "Document uploaded. Verification started."
}
```

### Run Verification
```http
POST /api/v1/verify
Content-Type: application/json

{
  "document_id": "doc_abc123",
  "language_hint": "hi",
  "document_type_hint": "aadhaar_card",
  "run_fraud_check": true
}
```

```json
{
  "verification_id": "ver_xyz789",
  "document_id": "doc_abc123",
  "status": "verified",
  "overall_confidence": 0.92,
  "document_type": "aadhaar_card",
  "extracted_fields": {
    "name": "राजेश कुमार",
    "aadhaar_number": "1234 5678 9012",
    "dob": "1990-05-15",
    "gender": "Male",
    "address": "123 मुख्य सड़क, चेन्नई"
  },
  "validation_results": {
    "aadhaar_number": {"status": "valid", "message": "Checksum verified"},
    "name": {"status": "valid"},
    "dob": {"status": "valid"}
  },
  "fraud_check": {
    "risk_level": "low",
    "score": 0.08,
    "flags": []
  },
  "processing_time_ms": 1847
}
```

---

# 9. MCP Server Specification

## 9.1 Server Configuration

```python
mcp = FastMCP("docverify_mcp")

# Transport: Streamable HTTP on port 8001
# Run: python -m src.mcp.server --http --port 8001
```

## 9.2 Tools

### Tool 1: docverify_ocr_extract
```yaml
Name: docverify_ocr_extract
Description: Extract text from document image using multi-language OCR
Inputs:
  - image_base64: string (required) - Base64 encoded image
  - language_hint: enum [en, hi, ta, te] (optional)
  - preprocess: boolean (default: true)
  - response_format: enum [json, markdown] (default: json)
Output: Extracted text with confidence and bounding boxes
```

### Tool 2: docverify_classify_document
```yaml
Name: docverify_classify_document
Description: Classify document type
Inputs:
  - ocr_text: string (required)
  - image_base64: string (optional)
  - use_vision: boolean (default: true)
Output: Document type with confidence and reasoning
```

### Tool 3: docverify_extract_fields
```yaml
Name: docverify_extract_fields
Description: Extract structured fields from document
Inputs:
  - ocr_text: string (required)
  - document_type: enum (required)
  - language: enum (default: en)
Output: Field values with confidence scores
```

### Tool 4: docverify_validate_fields
```yaml
Name: docverify_validate_fields
Description: Validate extracted fields
Inputs:
  - document_type: enum (required)
  - fields: object (required)
  - strict_mode: boolean (default: false)
Output: Validation status per field
```

### Tool 5: docverify_check_fraud
```yaml
Name: docverify_check_fraud
Description: Perform fraud detection checks
Inputs:
  - document_id: string (optional)
  - image_base64: string (optional)
  - ocr_text: string (optional)
  - check_duplicates: boolean (default: true)
  - check_tampering: boolean (default: true)
Output: Fraud risk score and findings
```

### Tool 6: docverify_detect_stamps
```yaml
Name: docverify_detect_stamps
Description: Detect stamps and signatures
Inputs:
  - image_base64: string (required)
  - detect_stamps: boolean (default: true)
  - detect_signatures: boolean (default: true)
Output: Detected elements with positions
```

### Tool 7: docverify_full_verification
```yaml
Name: docverify_full_verification
Description: Run complete verification pipeline
Inputs:
  - image_base64: string (required)
  - language_hint: enum (optional)
  - document_type_hint: enum (optional)
  - run_fraud_check: boolean (default: true)
Output: Complete verification result
```

---

# 10. Project Structure

```
docverify-ai/
│
├── 📄 README.md
├── 📄 PRD.md                         # This document
├── 📄 pyproject.toml
├── 📄 .env.example
├── 📄 .gitignore
│
├── 📁 src/
│   ├── 📁 core/
│   │   ├── __init__.py
│   │   ├── config.py                 # Environment settings
│   │   ├── logger.py                 # Structured logging
│   │   └── exceptions.py             # Custom exceptions
│   │
│   ├── 📁 database/
│   │   ├── __init__.py
│   │   ├── client.py                 # Supabase client
│   │   ├── models.py                 # Pydantic models
│   │   └── repositories/
│   │       ├── document_repo.py
│   │       ├── verification_repo.py
│   │       └── audit_repo.py
│   │
│   ├── 📁 preprocessing/
│   │   ├── __init__.py
│   │   ├── deskew.py
│   │   ├── denoise.py
│   │   ├── enhance.py
│   │   └── pipeline.py
│   │
│   ├── 📁 ocr/
│   │   ├── __init__.py
│   │   ├── base.py                   # Abstract interface
│   │   ├── paddle_ocr.py
│   │   ├── easy_ocr.py
│   │   ├── ensemble.py
│   │   └── language_detector.py
│   │
│   ├── 📁 classification/
│   │   ├── __init__.py
│   │   ├── classifier.py
│   │   ├── template_matcher.py
│   │   └── templates/                # JSON templates
│   │
│   ├── 📁 extraction/
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   ├── ner_model.py
│   │   ├── regex_patterns.py
│   │   └── field_types/
│   │
│   ├── 📁 validation/
│   │   ├── __init__.py
│   │   ├── validator.py
│   │   ├── llm_validator.py
│   │   └── rules/
│   │
│   ├── 📁 detection/
│   │   ├── __init__.py
│   │   ├── stamp_detector.py
│   │   └── signature_detector.py
│   │
│   ├── 📁 fraud/
│   │   ├── __init__.py
│   │   ├── tamper_detector.py
│   │   ├── duplicate_checker.py
│   │   └── embedding_store.py
│   │
│   ├── 📁 llm/
│   │   ├── __init__.py
│   │   ├── gemini_client.py
│   │   ├── ollama_client.py
│   │   ├── prompts/
│   │   └── chains/
│   │
│   ├── 📁 orchestration/
│   │   ├── __init__.py
│   │   ├── pipeline.py
│   │   ├── agents/
│   │   └── tools/
│   │
│   ├── 📁 api/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── middleware/
│   │
│   └── 📁 mcp/
│       ├── __init__.py
│       ├── server.py                 # MCP server
│       ├── tools/
│       └── resources/
│
├── 📁 ui/
│   ├── app.py                        # Streamlit main
│   ├── pages/
│   ├── components/
│   └── styles/
│
├── 📁 tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── 📁 scripts/
│   ├── setup_supabase.py
│   ├── download_models.py
│   └── generate_samples.py
│
└── 📁 docs/
    ├── API.md
    └── MCP_INTEGRATION.md
```

---

# 11. 15-Day Development Roadmap

## Team Allocation

- **Dev A:** Backend, OCR, LLM, MCP Server
- **Dev B:** Database, Preprocessing, UI, Validation

## Phase 1: Foundation (Days 1-3)

### Day 1: Project Setup
| Dev A | Dev B |
|-------|-------|
| Initialize project structure | Setup Supabase project |
| Setup Poetry + dependencies | Create database schema |
| Configure Ollama + models | Setup environment variables |
| Test Gemini API connection | Create .env templates |

**Milestone:** Both devs can run `poetry install` and connect to services

### Day 2: Core Infrastructure
| Dev A | Dev B |
|-------|-------|
| Implement `core/config.py` | Implement `database/client.py` |
| Implement `core/logger.py` | Implement `database/models.py` |
| Setup LangChain base | Create repository classes |
| Setup LlamaIndex base | Test Supabase CRUD |

**Milestone:** Logging works, database reads/writes work

### Day 3: Basic API + UI Shell
| Dev A | Dev B |
|-------|-------|
| Create FastAPI app skeleton | Create Streamlit app skeleton |
| Implement health endpoints | Build upload page |
| Setup API schemas | Build basic result display |
| Test file upload endpoint | Style with custom CSS |

**Milestone:** Can upload a file via UI, it reaches API

## Phase 2: OCR & Preprocessing (Days 4-6)

### Day 4: Image Preprocessing
| Dev A | Dev B |
|-------|-------|
| Implement deskew module | Implement denoise module |
| Implement enhance module | Implement normalize module |
| Create preprocessing pipeline | Test with sample images |
| Handle PDF to image | Save preprocessed images |

**Milestone:** Upload image → Get preprocessed version

### Day 5: OCR Implementation
| Dev A | Dev B |
|-------|-------|
| Implement PaddleOCR wrapper | Implement EasyOCR wrapper |
| Implement Tesseract wrapper | Implement language detector |
| Create base OCR interface | Test each OCR engine |
| Build OCR ensemble logic | Compare accuracy |

**Milestone:** Get text from images in Hindi/English/Tamil/Telugu

### Day 6: OCR Pipeline Integration
| Dev A | Dev B |
|-------|-------|
| Integrate preprocessing + OCR | Save OCR results to DB |
| Add confidence scoring | Build OCR result viewer in UI |
| Implement retry logic | Show confidence meters |
| Test with various documents | Handle errors gracefully |

**Milestone:** End-to-end: Upload → Preprocess → OCR → View text

## Phase 3: Classification & Extraction (Days 7-9)

### Day 7: Document Classification
| Dev A | Dev B |
|-------|-------|
| Design classification prompts | Create document templates |
| Implement Gemini classifier | Define template schemas |
| Build template matcher | Store templates in DB |
| Test classification accuracy | Build classification UI display |

**Milestone:** Upload → Auto-detect document type

### Day 8: Field Extraction
| Dev A | Dev B |
|-------|-------|
| Implement name extractor | Implement date extractor |
| Implement ID number extractor | Implement address extractor |
| Build NER integration | Create regex patterns |
| Combine extraction strategies | Test field extraction |

**Milestone:** Extract key fields from classified documents

### Day 9: LLM-Enhanced Extraction
| Dev A | Dev B |
|-------|-------|
| Build extraction prompts | Create extraction chains |
| Implement Gemini extraction | Handle multi-language fields |
| Add Ollama fallback | Display extracted fields in UI |
| Test accuracy on Tier 1 languages | Add field confidence display |

**Milestone:** High-quality field extraction with confidence scores

## Phase 4: Validation & Detection (Days 10-12)

### Day 10: Field Validation
| Dev A | Dev B |
|-------|-------|
| Implement Aadhaar validation rules | Implement PAN validation rules |
| Implement date validation | Implement name validation |
| Build LLM validation chain | Create validation result schema |
| Test validation logic | Display validation results in UI |

**Milestone:** Fields are validated with pass/fail + reasons

### Day 11: Stamp & Signature Detection
| Dev A | Dev B |
|-------|-------|
| Implement stamp detector | Implement signature detector |
| Train/configure detection model | Define seal templates |
| Build position validation | Test detection accuracy |
| Integrate with pipeline | Show detections in UI overlay |

**Milestone:** Detect and highlight stamps/signatures

### Day 12: Fraud Detection Basics
| Dev A | Dev B |
|-------|-------|
| Implement tamper detector | Implement duplicate checker |
| Build consistency checker | Setup vector embeddings |
| Create fraud scoring | Store embeddings in pgvector |
| Test fraud detection | Show fraud flags in UI |

**Milestone:** Basic fraud detection working

## Phase 5: MCP Server & Polish (Days 13-14)

### Day 13: MCP Server Implementation
| Dev A | Dev B |
|-------|-------|
| Setup FastMCP server | Create Pydantic models for MCP |
| Implement OCR tools | Implement validation tools |
| Implement classification tools | Implement fraud tools |
| Test with MCP Inspector | Document tool schemas |

**Milestone:** MCP server running with all core tools

### Day 14: Integration & Orchestration
| Dev A | Dev B |
|-------|-------|
| Build verification agent | Create full pipeline orchestration |
| Integrate all tools | Add analytics dashboard |
| Setup tool calling chain | Build audit log viewer |
| End-to-end testing | Performance optimization |

**Milestone:** Full pipeline: Upload → Verify → Results + MCP works

## Phase 6: Testing & Demo (Day 15)

### Day 15: Final Polish
| Both Developers |
|-----------------|
| Generate synthetic test documents |
| Run full system tests |
| Fix critical bugs |
| Record demo video |
| Write documentation |
| Deploy to Jarvis Labs |

**Milestone:** Demo-ready product!

---

# 12. Module Specifications

## 12.1 Config Module (`src/core/config.py`)

```python
class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_key: str
    
    # Gemini
    google_api_key: str
    gemini_model: str = "gemini-2.0-flash-exp"
    
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    
    # OCR
    default_ocr_engine: str = "paddleocr"
    ocr_languages: str = "en,hi,ta,te"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
```

## 12.2 OCR Module (`src/ocr/`)

```python
@dataclass
class OCRResult:
    text: str
    confidence: float
    language: str
    blocks: list[TextBlock]
    processing_time_ms: int
    engine: str

class BaseOCR(ABC):
    @abstractmethod
    async def extract_text(self, image: np.ndarray) -> OCRResult:
        pass

class PaddleOCREngine(BaseOCR):
    # Primary OCR implementation
    
class EasyOCREngine(BaseOCR):
    # Fallback OCR implementation

class OCREnsemble:
    # Combines multiple engines
```

## 12.3 LLM Module (`src/llm/`)

```python
class GeminiClient:
    async def generate(self, prompt: str) -> LLMResponse
    async def generate_with_image(self, prompt: str, image: str) -> LLMResponse
    async def generate_json(self, prompt: str, schema: dict) -> dict

class OllamaClient:
    # Same interface for local LLM

class LLMFactory:
    @classmethod
    def get_primary(cls) -> BaseLLMClient  # Gemini
    
    @classmethod
    def get_local(cls) -> BaseLLMClient    # Ollama
```

## 12.4 Classification Module (`src/classification/`)

```python
class DocumentType(str, Enum):
    BIRTH_CERTIFICATE = "birth_certificate"
    AADHAAR_CARD = "aadhaar_card"
    PAN_CARD = "pan_card"
    # ...

@dataclass
class ClassificationResult:
    document_type: DocumentType
    confidence: float
    reasoning: str

class DocumentClassifier:
    async def classify(self, ocr_text: str, image: np.ndarray = None) -> ClassificationResult
```

---

# 13. Success Metrics

## 13.1 Technical Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| OCR Accuracy (English) | >95% | Character-level accuracy |
| OCR Accuracy (Hindi) | >90% | Character-level accuracy |
| OCR Accuracy (Tamil/Telugu) | >85% | Character-level accuracy |
| Classification Accuracy | >92% | Correct document type |
| Field Extraction Accuracy | >88% | Correct field values |
| Fraud Detection Recall | >80% | Catch fraudulent docs |
| Average Processing Time | <10s | End-to-end verification |
| API Response Time (p95) | <500ms | Single API call |

## 13.2 Business Metrics

| Metric | Target |
|--------|--------|
| Documents Processed | 100+/day capacity |
| Verification Success Rate | >85% auto-verified |
| Manual Review Rate | <15% |
| False Positive Rate | <5% |

---

# 14. MVP Scope

## 14.1 Included in MVP

- ✅ Multi-language OCR (Hindi, English, Tamil, Telugu)
- ✅ Image preprocessing pipeline
- ✅ Document classification (5+ types)
- ✅ Field extraction + validation
- ✅ Basic stamp/signature detection
- ✅ Duplicate detection via embeddings
- ✅ Streamlit dashboard
- ✅ MCP Server with core tools
- ✅ Supabase integration
- ✅ Audit logging

## 14.2 Deferred to Post-MVP

- ❌ Offline/edge deployment
- ❌ Advanced fraud detection ML models
- ❌ Physical document scanning
- ❌ Authentication & RBAC
- ❌ Multi-tenant support
- ❌ Advanced analytics
- ❌ Batch processing queue
- ❌ Webhook integrations
- ❌ Tier 2/3 language support

---

# 15. Setup Instructions

## 15.1 Prerequisites

- Python 3.11+
- Git
- GPU with 8GB+ VRAM (for Ollama)
- Accounts: GitHub, Supabase, Google AI Studio

## 15.2 Quick Setup

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/docverify-ai.git
cd docverify-ai

# 2. Install dependencies
poetry install

# 3. Install Ollama & models
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3.1:8b
ollama pull nomic-embed-text

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run services
uvicorn src.api.main:app --reload --port 8000
streamlit run ui/app.py --server.port 8501
python -m src.mcp.server --http --port 8001
```

## 15.3 API Keys Required

| Service | URL | Free Tier |
|---------|-----|-----------|
| Gemini | https://aistudio.google.com/apikey | Yes |
| Supabase | https://supabase.com | Yes |

---

# 16. Quick Reference

## 16.1 Daily Commands

```bash
# Start development
cd ~/docverify-ai
git pull origin main
poetry shell
ollama serve &

# Run services (3 terminals)
uvicorn src.api.main:app --reload --port 8000
streamlit run ui/app.py --server.port 8501
python -m src.mcp.server --http --port 8001

# Save work
git add .
git commit -m "feat: description"
git push origin main
```

## 16.2 Test Commands

```bash
# Test OCR
python -c "from paddleocr import PaddleOCR; print('OK')"

# Test Gemini
python -c "
import os; from dotenv import load_dotenv; load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
print(genai.GenerativeModel('gemini-2.0-flash-exp').generate_content('Hi').text)
"

# Test Ollama
ollama run llama3.1:8b "Hello"

# Test MCP
npx @modelcontextprotocol/inspector
```

## 16.3 Key URLs

- API Docs: http://localhost:8000/docs
- Streamlit: http://localhost:8501
- MCP: http://localhost:8001

---

# Appendix A: Document Templates

## Aadhaar Card Schema

```json
{
  "document_type": "aadhaar_card",
  "fields": {
    "name": {"type": "string", "required": true},
    "aadhaar_number": {"type": "string", "pattern": "^\\d{4}\\s?\\d{4}\\s?\\d{4}$", "required": true},
    "dob": {"type": "date", "required": true},
    "gender": {"type": "enum", "values": ["Male", "Female", "Other"], "required": true},
    "address": {"type": "string", "required": true}
  },
  "validation_rules": {
    "aadhaar_number": "verhoeff_checksum"
  }
}
```

## PAN Card Schema

```json
{
  "document_type": "pan_card",
  "fields": {
    "name": {"type": "string", "required": true},
    "pan_number": {"type": "string", "pattern": "^[A-Z]{5}[0-9]{4}[A-Z]$", "required": true},
    "father_name": {"type": "string", "required": true},
    "dob": {"type": "date", "required": true}
  }
}
```

---

# Appendix B: Validation Rules

## Aadhaar Number Validation (Verhoeff Checksum)

```python
def validate_aadhaar(number: str) -> bool:
    """
    Validate Aadhaar number using Verhoeff algorithm.
    Aadhaar is 12 digits with last digit as checksum.
    """
    # Remove spaces
    number = number.replace(" ", "")
    
    if len(number) != 12 or not number.isdigit():
        return False
    
    # Verhoeff multiplication table
    d = [
        [0,1,2,3,4,5,6,7,8,9],
        [1,2,3,4,0,6,7,8,9,5],
        # ... full table
    ]
    
    # Verhoeff permutation table
    p = [
        [0,1,2,3,4,5,6,7,8,9],
        # ... full table
    ]
    
    # Calculate checksum
    c = 0
    for i, digit in enumerate(reversed(number)):
        c = d[c][p[i % 8][int(digit)]]
    
    return c == 0
```

## PAN Format Validation

```python
import re

def validate_pan(pan: str) -> bool:
    """
    Validate PAN format: XXXXX0000X
    - First 3: Alpha (AAA-ZZZ)
    - 4th: C/P/H/F/A/T/B/L/J/G (entity type)
    - 5th: Alpha (first letter of surname)
    - 6-9: Numeric (0001-9999)
    - 10th: Alpha (check letter)
    """
    pattern = r'^[A-Z]{3}[CPHFATBLJ][A-Z]\d{4}[A-Z]$'
    return bool(re.match(pattern, pan.upper()))
```

---

# Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2025 | Team | Initial PRD |

---

**End of PRD**
