-- DocVerify AI - Supabase Database Schema
-- Run this script in the Supabase SQL Editor to set up the database

-- Enable pgvector extension for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Document Types Enum
DO $$ BEGIN
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
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Verification Status Enum
DO $$ BEGIN
    CREATE TYPE verification_status AS ENUM (
        'pending',
        'processing',
        'verified',
        'rejected',
        'manual_review'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Documents Table
CREATE TABLE IF NOT EXISTS documents (
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
CREATE TABLE IF NOT EXISTS verifications (
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
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    verification_id UUID REFERENCES verifications(id) ON DELETE SET NULL,

    action VARCHAR(100) NOT NULL,
    actor_id UUID,
    actor_type VARCHAR(50) DEFAULT 'system',

    details JSONB,
    ip_address INET,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Document Templates Table
CREATE TABLE IF NOT EXISTS document_templates (
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

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(document_type);
CREATE INDEX IF NOT EXISTS idx_documents_hash ON documents(file_hash);
CREATE INDEX IF NOT EXISTS idx_documents_created ON documents(created_at DESC);

-- Vector similarity index (requires pgvector)
-- Uncomment after adding embeddings:
-- CREATE INDEX IF NOT EXISTS idx_documents_embedding ON documents
--     USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_verifications_status ON verifications(status);
CREATE INDEX IF NOT EXISTS idx_verifications_document ON verifications(document_id);
CREATE INDEX IF NOT EXISTS idx_verifications_created ON verifications(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_audit_document ON audit_logs(document_id);
CREATE INDEX IF NOT EXISTS idx_audit_verification ON audit_logs(verification_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at DESC);

-- Row Level Security (RLS) Policies
-- Enable RLS on all tables
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE verifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_templates ENABLE ROW LEVEL SECURITY;

-- For MVP: Allow all access (adjust for production with proper auth)
CREATE POLICY IF NOT EXISTS "Allow all access to documents" ON documents FOR ALL USING (true);
CREATE POLICY IF NOT EXISTS "Allow all access to verifications" ON verifications FOR ALL USING (true);
CREATE POLICY IF NOT EXISTS "Allow all access to audit_logs" ON audit_logs FOR ALL USING (true);
CREATE POLICY IF NOT EXISTS "Allow all access to document_templates" ON document_templates FOR ALL USING (true);

-- Updated At Trigger Function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to documents table
DROP TRIGGER IF EXISTS update_documents_updated_at ON documents;
CREATE TRIGGER update_documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to verifications table
DROP TRIGGER IF EXISTS update_verifications_updated_at ON verifications;
CREATE TRIGGER update_verifications_updated_at
    BEFORE UPDATE ON verifications
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert default document templates
INSERT INTO document_templates (document_type, template_name, language, field_schema, validation_rules)
VALUES
    ('aadhaar_card', 'Aadhaar Card - Standard', 'en', '{
        "fields": {
            "name": {"type": "string", "required": true},
            "aadhaar_number": {"type": "string", "pattern": "^\\d{4}\\s?\\d{4}\\s?\\d{4}$", "required": true},
            "dob": {"type": "date", "required": true},
            "gender": {"type": "enum", "values": ["Male", "Female", "Other"], "required": true},
            "address": {"type": "string", "required": true}
        }
    }', '{"aadhaar_number": "verhoeff_checksum"}'),

    ('pan_card', 'PAN Card - Standard', 'en', '{
        "fields": {
            "name": {"type": "string", "required": true},
            "pan_number": {"type": "string", "pattern": "^[A-Z]{5}[0-9]{4}[A-Z]$", "required": true},
            "father_name": {"type": "string", "required": true},
            "dob": {"type": "date", "required": true}
        }
    }', '{"pan_number": "format_regex"}'),

    ('voter_id', 'Voter ID - Standard', 'en', '{
        "fields": {
            "name": {"type": "string", "required": true},
            "voter_id_number": {"type": "string", "pattern": "^[A-Z]{3}[0-9]{7}$", "required": true},
            "father_name": {"type": "string", "required": false},
            "age": {"type": "integer", "required": false}
        }
    }', '{"voter_id_number": "format_regex"}'),

    ('driving_license', 'Driving License - Standard', 'en', '{
        "fields": {
            "name": {"type": "string", "required": true},
            "dl_number": {"type": "string", "required": true},
            "dob": {"type": "date", "required": true},
            "valid_upto": {"type": "date", "required": true}
        }
    }', '{"dl_number": "format_regex", "valid_upto": "future_date"}'),

    ('passport', 'Passport - Standard', 'en', '{
        "fields": {
            "name": {"type": "string", "required": true},
            "passport_number": {"type": "string", "pattern": "^[A-Z][0-9]{7}$", "required": true},
            "dob": {"type": "date", "required": true},
            "surname": {"type": "string", "required": true},
            "given_name": {"type": "string", "required": true}
        }
    }', '{"passport_number": "format_regex"}'),

    ('birth_certificate', 'Birth Certificate - Standard', 'en', '{
        "fields": {
            "child_name": {"type": "string", "required": true},
            "dob": {"type": "date", "required": true},
            "place_of_birth": {"type": "string", "required": true},
            "father_name": {"type": "string", "required": false},
            "mother_name": {"type": "string", "required": false},
            "registration_number": {"type": "string", "required": false}
        }
    }', '{}')
ON CONFLICT DO NOTHING;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'DocVerify AI database schema created successfully!';
END $$;
